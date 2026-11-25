import datetime
import logging
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from backend.app.core.config import atomic_write_json_file, read_json_file, settings
from backend.app.schemas.srs import (
    RATING_METADATA,
    SrsCardRecord,
    SrsDueCardItem,
    SrsDueResponse,
    SrsRateRequest,
    SrsRateResponse,
    SrsRating,
    SrsStatsResponse,
)
from backend.app.services.content_service import content_service

logger = logging.getLogger('academy.srs')

# Начальные коэффициенты стабильности памяти FSRS для первой сессии
INITIAL_STABILITY: Dict[int, float] = {
    SrsRating.AGAIN: 0.4,   # 1: «Не вспомнил» — повтор в тот же день
    SrsRating.HARD: 1.2,    # 2: «Со скрипом» — 1-2 дня
    SrsRating.GOOD: 3.2,    # 3: «Вспомнил» — ~3 дня
    SrsRating.EASY: 7.5,    # 4: «На автомате» — неделя
}

# Начисление опыта XP за когнитивную нагрузку при повторении
XP_REWARD_BY_RATING: Dict[int, int] = {
    SrsRating.AGAIN: 5,
    SrsRating.HARD: 8,
    SrsRating.GOOD: 12,
    SrsRating.EASY: 15,
}


def _today_iso() -> str:
    return datetime.date.today().isoformat()


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class SrsService:
    """
    Канонический сервис интервального повторения на базе современной модели FSRS.
    Управляет расчётом стабильности (S), сложности (D), очередей повторения
    и начислением опыта (+XP) со стриком.
    """

    def __init__(self, data_dir: Optional[Path] = None) -> None:
        self.srs_dir = (data_dir or settings.DATA_DIR) / 'srs'
        self.cards_file = self.srs_dir / 'cards_state.json'
        self.stats_file = self.srs_dir / 'user_stats.json'
        self._cards_cache: Optional[Dict[str, Dict[str, Any]]] = None
        self._stats_cache: Optional[Dict[str, Any]] = None

    def _ensure_dir(self) -> None:
        self.srs_dir.mkdir(parents=True, exist_ok=True)

    def _get_cards_data(self) -> Dict[str, Dict[str, Any]]:
        if self._cards_cache is None:
            self._ensure_dir()
            data = read_json_file(self.cards_file, default={}, logger=logger)
            self._cards_cache = data if isinstance(data, dict) else {}
        return self._cards_cache

    def _save_cards_data(self) -> None:
        if self._cards_cache is not None:
            self._ensure_dir()
            atomic_write_json_file(self.cards_file, self._cards_cache)

    def _get_stats_data(self) -> Dict[str, Any]:
        if self._stats_cache is None:
            self._ensure_dir()
            data = read_json_file(self.stats_file, default=None, logger=logger)
            if not isinstance(data, dict):
                data = {
                    'xp_total': 0,
                    'streak_days': 0,
                    'last_active_date': None,
                    'total_reviewed_count': 0,
                    'successful_recall_count': 0,
                    'daily_reviewed_history': {},
                }
            self._stats_cache = data
        return self._stats_cache

    def _save_stats_data(self) -> None:
        if self._stats_cache is not None:
            self._ensure_dir()
            atomic_write_json_file(self.stats_file, self._stats_cache)

    def get_card_state(self, card_id: str) -> Optional[SrsCardRecord]:
        cards = self._get_cards_data()
        raw = cards.get(card_id)
        if not raw:
            return None
        return SrsCardRecord.model_validate(raw)

    def calculate_fsrs_transition(
        self,
        current_record: Optional[SrsCardRecord],
        rating: int,
        deck_id: str,
        card_id: str,
    ) -> Tuple[float, float, int, str]:
        """
        Математический переход состояния FSRS:
        Возвращает: (new_stability, new_difficulty, interval_days, due_date)
        """
        today_date = datetime.date.today()

        if current_record is None or current_record.reps == 0:
            # Первая встреча с карточкой
            new_s = INITIAL_STABILITY.get(rating, 2.5)
            # Сложность D от 1.0 до 10.0 (средняя 5.0)
            d_delta = (3 - rating) * 1.2
            new_d = max(1.0, min(10.0, 5.0 + d_delta))
            interval_days = max(1, round(new_s)) if rating > SrsRating.AGAIN else 0
        else:
            prev_s = max(0.2, current_record.stability)
            prev_d = current_record.difficulty

            # 1. Корректировка сложности: чем ниже оценка, тем выше сложность
            d_delta = (3 - rating) * 0.9
            # Возврат к среднему значению D=5.0 для предотвращения насыщения
            new_d = max(1.0, min(10.0, prev_d + d_delta))

            # 2. Корректировка стабильности памяти S
            if rating == SrsRating.AGAIN:
                # Забывание: сброс стабильности с учётом предыдущего фундамента
                new_s = max(0.4, prev_s * 0.3)
                interval_days = 0
            else:
                # Успешное припоминание: рост стабильности
                # Множитель сложности: легкие карточки масштабируются быстрее
                diff_factor = max(0.5, (11.0 - new_d) / 5.0)
                # Множитель оценки: 2(hard)=1.2, 3(good)=2.2, 4(easy)=3.5
                rating_multiplier = 1.0 + (rating - 1.5) * 0.85
                new_s = prev_s * (1.0 + diff_factor * rating_multiplier * 0.6)
                interval_days = max(1, round(new_s))

        # Вычисление даты следующего показа
        next_due = today_date + datetime.timedelta(days=interval_days)
        due_date_str = next_due.isoformat()
        return round(new_s, 2), round(new_d, 2), interval_days, due_date_str

    def rate_card(self, payload: SrsRateRequest) -> SrsRateResponse:
        """
        Основной бизнес-метод фиксации оценки обучающегося по карточке.
        Обновляет модель FSRS, начисляет XP и стрик, атомарно сохраняет данные.
        """
        card_id = payload.card_id
        deck_id = payload.deck_id
        rating = payload.rating

        cards_data = self._get_cards_data()
        existing_raw = cards_data.get(card_id)
        current_record = SrsCardRecord.model_validate(existing_raw) if existing_raw else None

        new_s, new_d, interval_days, due_date = self.calculate_fsrs_transition(
            current_record=current_record,
            rating=rating,
            deck_id=deck_id,
            card_id=card_id,
        )

        reps = (current_record.reps + 1) if (current_record and rating > SrsRating.AGAIN) else (0 if rating == SrsRating.AGAIN else 1)
        lapses = ((current_record.lapses + 1) if current_record else 1) if rating == SrsRating.AGAIN else (current_record.lapses if current_record else 0)
        state_label = 'relearning' if rating == SrsRating.AGAIN else ('review' if reps > 2 else 'learning')

        updated_record = SrsCardRecord(
            card_id=card_id,
            deck_id=deck_id,
            stability=new_s,
            difficulty=new_d,
            reps=reps,
            lapses=lapses,
            state=state_label,
            due_date=due_date,
            interval_days=interval_days,
            last_reviewed=_now_iso(),
        )

        cards_data[card_id] = updated_record.model_dump()
        self._save_cards_data()

        # Обновление пользовательской статистики (XP и стрик)
        xp_gain = XP_REWARD_BY_RATING.get(rating, 10)
        stats = self._get_stats_data()
        today_str = _today_iso()

        stats['xp_total'] = int(stats.get('xp_total', 0)) + xp_gain
        stats['total_reviewed_count'] = int(stats.get('total_reviewed_count', 0)) + 1
        if rating > SrsRating.AGAIN:
            stats['successful_recall_count'] = int(stats.get('successful_recall_count', 0)) + 1

        # Обновление суточной истории
        daily_map = stats.setdefault('daily_reviewed_history', {})
        daily_map[today_str] = int(daily_map.get(today_str, 0)) + 1

        # Логика стрика
        last_active = stats.get('last_active_date')
        streak = int(stats.get('streak_days', 0))

        if not last_active:
            streak = 1
        elif last_active != today_str:
            try:
                last_dt = datetime.date.fromisoformat(last_active)
                diff_days = (datetime.date.today() - last_dt).days
                if diff_days == 1:
                    streak += 1
                elif diff_days > 1:
                    streak = 1
            except Exception:
                streak = 1
        stats['last_active_date'] = today_str
        stats['streak_days'] = streak
        self._save_stats_data()

        meta = RATING_METADATA.get(rating, {'label': 'Оценено'})
        rating_label = meta['label']

        return SrsRateResponse(
            ok=True,
            card_id=card_id,
            rating=rating,
            rating_label=rating_label,
            new_stability=new_s,
            new_difficulty=new_d,
            interval_days=interval_days,
            due_date=due_date,
            xp_awarded=xp_gain,
            streak_days=streak,
            message=f'Карточка оценена: «{rating_label}». Следующий повтор через {interval_days} дн. (+{xp_gain} XP)',
        )

    def get_due_cards(
        self,
        echelon_filter: Optional[int] = None,
        deck_filter: Optional[str] = None,
        limit: int = 50,
    ) -> SrsDueResponse:
        """
        Формирует очередь карточек на сегодня.
        Если сохранённых карточек меньше лимита, подмешивает карточки из базы контента.
        """
        today_str = _today_iso()
        cards_data = self._get_cards_data()
        all_decks = content_service.get_cards()

        due_items: List[SrsDueCardItem] = []
        echelon_counts: Dict[str, int] = {'1': 0, '2': 0, '3': 0, '4': 0}

        # 1. Поиск сохранённых карточек, у которых наступила дата повторения
        for cid, record_dict in cards_data.items():
            due_date = record_dict.get('due_date', '')
            if due_date <= today_str:
                deck_id = record_dict.get('deck_id', '')
                if deck_filter and deck_id != deck_filter:
                    continue

                deck = all_decks.get(deck_id, {})
                deck_cards = deck.get('cards', [])
                deck_title = deck.get('title', deck_id)

                # Извлечение вопроса и ответа
                card_q = 'Вопрос'
                card_a = 'Ответ'
                if '#' in cid:
                    try:
                        idx = int(cid.split('#')[1])
                        if 0 <= idx < len(deck_cards):
                            card_q = deck_cards[idx].get('q', card_q)
                            card_a = deck_cards[idx].get('a', card_a)
                    except Exception:
                        pass

                # Определение эшелона по ID колоды
                ech = 1
                if any(x in deck_id for x in ['Ф-04', 'Ф-05', 'Ф-06', 'Ф-07', 'Ф-08']):
                    ech = 2
                elif any(x in deck_id for x in ['Ф-09', 'Ф-10', 'Ф-11', 'Ф-12']):
                    ech = 3
                elif any(x in deck_id for x in ['Ф-13', 'Ф-14', 'Ф-15']):
                    ech = 4

                if echelon_filter and ech != echelon_filter:
                    continue

                echelon_counts[str(ech)] = echelon_counts.get(str(ech), 0) + 1
                due_items.append(
                    SrsDueCardItem(
                        card_id=cid,
                        deck_id=deck_id,
                        deck_title=deck_title,
                        question=card_q,
                        answer=card_a,
                        echelon=ech,
                        stability=float(record_dict.get('stability', 0.0)),
                        difficulty=float(record_dict.get('difficulty', 5.0)),
                        reps=int(record_dict.get('reps', 0)),
                        is_due=True,
                    )
                )

        # 2. Если карточек к повторению мало, наполняем свежими из контента
        if len(due_items) < limit:
            for d_id, deck in all_decks.items():
                if deck_filter and d_id != deck_filter:
                    continue
                d_cards = deck.get('cards', [])
                d_title = deck.get('title', d_id)
                ech = 1
                if any(x in d_id for x in ['Ф-04', 'Ф-05', 'Ф-06', 'Ф-07', 'Ф-08']):
                    ech = 2
                elif any(x in d_id for x in ['Ф-09', 'Ф-10', 'Ф-11', 'Ф-12']):
                    ech = 3
                elif any(x in d_id for x in ['Ф-13', 'Ф-14', 'Ф-15']):
                    ech = 4

                if echelon_filter and ech != echelon_filter:
                    continue

                for idx, c in enumerate(d_cards):
                    cid = f'{d_id}#{idx}'
                    if cid not in cards_data:
                        echelon_counts[str(ech)] = echelon_counts.get(str(ech), 0) + 1
                        due_items.append(
                            SrsDueCardItem(
                                card_id=cid,
                                deck_id=d_id,
                                deck_title=d_title,
                                question=c.get('q', ''),
                                answer=c.get('a', ''),
                                echelon=ech,
                                stability=0.0,
                                difficulty=5.0,
                                reps=0,
                                is_due=True,
                            )
                        )
                        if len(due_items) >= limit:
                            break
                if len(due_items) >= limit:
                    break

        return SrsDueResponse(
            ok=True,
            due_count=len(due_items),
            echelon_counts=echelon_counts,
            cards=due_items,
        )

    def get_stats(self) -> SrsStatsResponse:
        """
        Возвращает агрегированные метрики успеваемости и ретеншна.
        """
        stats = self._get_stats_data()
        cards_data = self._get_cards_data()
        today_str = _today_iso()

        total_tracked = len(cards_data)
        due_today_count = sum(1 for c in cards_data.values() if c.get('due_date', '') <= today_str)

        daily_map = stats.get('daily_reviewed_history', {})
        reviewed_today = int(daily_map.get(today_str, 0))

        total_rev = int(stats.get('total_reviewed_count', 0))
        success_rev = int(stats.get('successful_recall_count', 0))
        retention = round((success_rev / total_rev * 100.0), 1) if total_rev > 0 else 100.0

        avg_diff = 5.0
        if total_tracked > 0:
            avg_diff = round(sum(float(c.get('difficulty', 5.0)) for c in cards_data.values()) / total_tracked, 2)

        return SrsStatsResponse(
            ok=True,
            total_cards_tracked=total_tracked,
            due_today=due_today_count,
            reviewed_today=reviewed_today,
            retention_rate_pct=retention,
            average_difficulty=avg_diff,
            streak_days=int(stats.get('streak_days', 0)),
            xp_total=int(stats.get('xp_total', 0)),
        )


srs_service = SrsService()
