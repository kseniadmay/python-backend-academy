import ast
import contextlib
import datetime
import io
import logging
import sys
import traceback
from typing import Any, Dict, List, Optional

from backend.app.core.config import atomic_write_json_file, read_json_file, settings
from backend.app.schemas.practice import (
    TaskDraftPayload,
    TaskDraftResponse,
    TaskHintResponse,
    TaskRunRequest,
    TaskRunResponse,
)
from backend.app.services.content_service import content_service
from backend.app.services.srs_service import srs_service
from backend.app.services.sync_service import sync_service

logger = logging.getLogger('academy.runner')


def _parse_socratic_hints(task: Dict[str, Any]) -> List[str]:
    """
    Извлекает список пошаговых наводок Сократа без готового кода.
    """
    raw_hint = task.get('hint') or ''
    if not raw_hint:
        return [
            'Внимательно проанализируйте сигнатуру целевой функции и типы входных параметров.',
            'Разбейте алгоритм на атомарные шаги: валидация входа -> трансформация данных -> возврат результата.',
            'Проверьте краевые случаи (пустые коллекции, None, неверные типы).'
        ]

    # Если хинт структурирован как «Шаг 1: ... Шаг 2: ...»
    if 'Шаг ' in raw_hint:
        parts = [p.strip() for p in raw_hint.split('Шаг ') if p.strip()]
        hints: List[str] = []
        for p in parts:
            clean = p.lstrip('0123456789:.- ')
            if clean:
                hints.append(clean)
        if hints:
            return hints

    return [raw_hint]


class CodeRunnerService:
    """
    Сервис изолированного серверного запуска и проверки задач Zen IDE.
    """

    def __init__(self) -> None:
        self.drafts_file = settings.DATA_DIR / 'user' / 'task_drafts.json'
        self._drafts_cache: Optional[Dict[str, str]] = None

    def _ensure_dir(self) -> None:
        self.drafts_file.parent.mkdir(parents=True, exist_ok=True)

    def _get_drafts(self) -> Dict[str, str]:
        if self._drafts_cache is None:
            self._ensure_dir()
            data = read_json_file(self.drafts_file, default={}, logger=logger)
            self._drafts_cache = data if isinstance(data, dict) else {}
        return self._drafts_cache

    def save_draft(self, payload: TaskDraftPayload) -> TaskDraftResponse:
        drafts = self._get_drafts()
        drafts[str(payload.task_id)] = payload.draft_code
        self._ensure_dir()
        atomic_write_json_file(self.drafts_file, drafts)
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        return TaskDraftResponse(ok=True, task_id=payload.task_id, saved_at=now_str)

    def get_draft(self, task_id: int) -> Optional[str]:
        return self._get_drafts().get(str(task_id))

    def get_hints(self, task_id: int, requested_level: int = 1) -> TaskHintResponse:
        task = content_service.get_task(task_id) or {}
        hints = _parse_socratic_hints(task)
        level = max(1, min(len(hints), requested_level))
        return TaskHintResponse(
            ok=True,
            task_id=task_id,
            total_hints=len(hints),
            hint_level=level,
            hints=hints[:level]
        )

    def run_task(self, payload: TaskRunRequest) -> TaskRunResponse:
        """
        Исполняет пользовательский код и сценарий тестов задачи.
        """
        task_id = payload.task_id
        user_code = payload.code

        task = content_service.get_task(task_id)
        if not task:
            return TaskRunResponse(
                ok=False,
                task_id=task_id,
                status='error',
                output='',
                error_message=f'Задача с ID {task_id} не найдена в базе курса',
            )

        test_code = task.get('tests') or ''
        socratic_hints = _parse_socratic_hints(task)
        first_hint = socratic_hints[0] if socratic_hints else None

        # 1. Синтаксический анализ кода обучающегося
        try:
            compiled_user = compile(user_code, '<user_code>', 'exec')
        except SyntaxError as syn_err:
            return TaskRunResponse(
                ok=True,
                task_id=task_id,
                status='fail',
                output=f'Синтаксическая ошибка (SyntaxError): {syn_err.msg}',
                error_message=f'Синтаксическая ошибка в строке {syn_err.lineno}: {syn_err.msg}',
                error_line=syn_err.lineno,
                socratic_hint=first_hint,
            )

        # 2. Изолированная среда исполнения
        stdout_capture = io.StringIO()
        exec_scope: Dict[str, Any] = {
            '__name__': '__main__',
            '__USER_CODE__': user_code,
            '__doc__': None,
        }

        # 3. Выполнение кода пользователя
        try:
            with contextlib.redirect_stdout(stdout_capture):
                exec(compiled_user, exec_scope)
        except Exception as exc:
            tb = traceback.format_exc()
            lineno = None
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                if frame.filename == '<user_code>':
                    lineno = frame.lineno
            return TaskRunResponse(
                ok=True,
                task_id=task_id,
                status='fail',
                output=f'{stdout_capture.getvalue()}\nИсключение во время работы кода:\n{tb}',
                error_message=f'{type(exc).__name__}: {exc}',
                error_line=lineno,
                socratic_hint=first_hint,
            )

        # 4. Выполнение проверочных тестов задачи
        if test_code:
            try:
                compiled_tests = compile(test_code, '<tests>', 'exec')
                with contextlib.redirect_stdout(stdout_capture):
                    exec(compiled_tests, exec_scope)
            except AssertionError as assert_err:
                msg = str(assert_err) or 'Проверочное условие (assert) не выполнено'
                return TaskRunResponse(
                    ok=True,
                    task_id=task_id,
                    status='fail',
                    output=stdout_capture.getvalue(),
                    error_message=msg,
                    socratic_hint=first_hint,
                )
            except Exception as test_exc:
                tb = traceback.format_exc()
                return TaskRunResponse(
                    ok=True,
                    task_id=task_id,
                    status='fail',
                    output=f'{stdout_capture.getvalue()}\nОшибка в ходе тестов: {tb}',
                    error_message=f'Ошибка тестирования: {test_exc}',
                    socratic_hint=first_hint,
                )

        # 5. Успешное прохождение: начисление наград и фиксация прогресса
        stats = srs_service._get_stats_data()
        current_streak = int(stats.get('streak_days', 1))

        # Сохранение задачи в sync_service
        sync_record = sync_service.read_sync_record()
        user_state = (sync_record.get('bundle', {}).get('academyState', {})) if sync_record else {}
        completed_tasks = user_state.get('completedTasks', [])
        is_first_solve = task_id not in completed_tasks

        xp_awarded = 15 if is_first_solve else 0
        if is_first_solve:
            completed_tasks.append(task_id)
            user_state['completedTasks'] = completed_tasks
            user_state['xp'] = int(user_state.get('xp', 0)) + 15

            # Обновление записи синхронизации
            sync_service.write_sync_record({
                'updatedAt': int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000),
                'device': 'fastapi-runner',
                'clientId': 'server-practice-engine',
                'bundle': {
                    'academyState': user_state,
                    'ideStatus': {str(task_id): 'passed'},
                    'ideDrafts': {str(task_id): user_code}
                }
            })

        output_text = stdout_capture.getvalue().strip()
        if not output_text:
            output_text = '✓ Все тесты пройдены чисто! Код соответствует требованиям спецификации.'

        return TaskRunResponse(
            ok=True,
            task_id=task_id,
            status='pass',
            output=output_text,
            error_message=None,
            xp_awarded=xp_awarded,
            streak_days=current_streak,
            socratic_hint=None,
        )


code_runner_service = CodeRunnerService()
