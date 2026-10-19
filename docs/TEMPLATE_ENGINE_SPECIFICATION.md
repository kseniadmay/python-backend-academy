# Спецификация движка шаблонов и системный промпт генератора (Academy Template Engine)

> **Статус:** Утвержденная архитектурная спецификация  
> **Связанный документ:** [`DESCRIPTOR_DECISIONS.md`](file:///Users/fury/OneDrive/Python_Backend_Academy/docs/DESCRIPTOR_DECISIONS.md) (Решение 23)

---

## 1. Архитектурная модель шагов Тропы

Каждый навык на Тропе Академии разворачивается через 4 универсальных мастер-шаблона:

```
               ЦЕПОЧКА ШАБЛОНОВ ПРОХОЖДЕНИЯ НАВЫКА
 ┌─────────────────────────────────────────────────────────────────┐
 │                      GlobalShellTemplate                        │
 │  • Адаптивный icon-only хедер (без схлопывания кнопок в div)    │
 │  • Семантический степпер с пиктограммами типов шагов            │
 └───────┬─────────────────────────┬─────────────────────────┬─────┘
         │                         │                         │
         ▼                         ▼                         ▼
 ┌───────────────┐        ┌─────────────────┐        ┌───────────────┐
 │TheoryTemplate │  ───>  │InitialFlashcard │  ───>  │ CodePractice  │
 │• Хук проблемы │        │    Template     │        │   Template    │
 │• O(1) vs O(N) │        │• До 7 карточек  │        │• Split-Tab    │
 │• MicroCheck   │        │• Intra-Session  │        │• Touch-свайп  │
 │  Gate (замок) │        │  Loop (доучи-   │        │• Атомарные    │
 │               │        │  вание в пачке) │        │  чипсы        │
 └───────────────┘        └─────────────────┘        └───────────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │ Внешний FSRS    │
                          │ тренажер        │
                          │ (через 24 часа) │
                          └─────────────────┘
```

---

## 2. DSL и TypeScript-контракты схемы данных

```typescript
export type StepType = 'THEORY' | 'INITIAL_FLASHCARDS' | 'CODE_PRACTICE' | 'MILESTONE_CHECKPOINT';

// 1. Конспект / Теория
export interface TheoryStepData {
  id: string;
  stepType: 'THEORY';
  topicTitle: string;
  hookHeadline: string;
  hookProblemStatement: string;
  practicalContrastSnippet: {
    language: 'python' | 'sql';
    code: string;
    annotation: string; // e.g. "O(1) in set vs O(N) in list"
  };
  backendTakeaway: string;
  microCheck: {
    prompt: string;
    options: { id: string; text: string }[];
    correctOptionId: string;
    explanation: string;
  };
  rewardXp: number; // 5-10 XP
}

// 2. Первичные карточки (Интродукция на Тропе)
export interface InitialFlashcard {
  id: string;
  question: string;
  coreAnswer: string;       // 1-2 предложения сути
  codeExample?: {
    badPractice?: string;   // Как делать не надо
    goodPractice: string;   // Идиоматичный код
  };
  backendInsight: string;   // Почему об этом спрашивают на собеседовании
}

export interface InitialFlashcardsStepData {
  stepType: 'INITIAL_FLASHCARDS';
  cards: InitialFlashcard[]; // ВАЛИДАЦИЯ: от 3 до 7 карточек!
  handoffToSrs: {
    srsTargetDeckId: string;
    firstReviewIntervalHours: number; // 24ч
  };
  rewardXp: number;
}

// 3. Практика в IDE
export interface CodePracticeStepData {
  stepType: 'CODE_PRACTICE';
  taskNumber: number;
  difficultyLevel: 1 | 2 | 3 | 4 | 5;
  taskInstruction: string;   // ВАЛИДАЦИЯ: запрещен глагол "Создайте X", если X в starterCode
  ioFlow: {
    inputLabel: string;
    inputValueFormatted: string;
    outputLabel: string;
    expectedOutputFormatted: string;
    stepNote?: string;
  };
  visualDiagram?: {
    type: 'SLICING_ANATOMY' | 'MEMORY_REFERENCE' | 'HASH_TABLE';
    title: string;
    payload: Record<string, unknown>;
  };
  scaffolding: {
    hints: [
      { level: 1; title: 'Вектор мысли'; content: string },
      { level: 2; title: 'Алгоритм'; content: string },
      { level: 3; title: 'Псевдокод'; content: string },
      { level: 4; title: 'Каркас решения'; content: string }
    ];
  };
  atomicSnippetChips: string[]; // ВАЛИДАЦИЯ: запрещено готовое решение целиком!
  starterCode: string;
  testCases: { id: string; desc: string; input: unknown; expected: unknown }[];
  rewardXp: number; // 20-35 XP
}
```

---

## 3. Мастер-промпт для AI-генератора уроков

Скопируйте этот блок для передачи AI-генератору уроков:

```markdown
### РОЛЬ
Ты — Lead Instructional Designer и Senior Content Engineer Академии Python Backend.
Твоя цель — генерировать контент учебных шагов в строгом соответствии с контрактами движка шаблонов.

---

### ПРАВИЛА И СТРОГИЕ ИНВАРИАНТЫ

1. КВАНТОВАНИЕ КАРТОЧЕК:
   - Максимум 5–7 карточек первичного ознакомления на один шаг.
   - Запрещено выдавать колоды по 15–20 карточек подряд. Если тема большая, разбей ее на шаги [Теория -> 5 карточек -> Задача IDE].

2. СТРУКТУРА ОБОРОТА КАРТОЧКИ:
   - `coreAnswer`: краткий прямой ответ без рассуждений.
   - `codeExample`: компактное сравнение «Было / Стало».
   - `backendInsight`: нюанс CPython, оптимизация аллокации памяти или вопрос скрининга.

3. ПРАКТИКА В IDE (КОДИНГ):
   - Устраняй коллизию формулировки: если переменная `original` объявлена в `starterCode`, пиши «Используя объявленный `original`, получите...». Запрещено писать «Создайте `original`».
   - Чипсы автокомплита (`atomicSnippetChips`): разрешены ТОЛЬКО атомарные токены (`[`, `]`, `:`, `-1`, `len`, `original`). СТРОГО ЗАПРЕЩЕНО помещать готовое решение задачи целиком (например, `original[::-1]`).
   - Наставник Сократ: ровно 4 прогрессивных уровня подсказок (от мысли к каркасу).

4. ТЕОРИЯ:
   - Включай заголовок-проблему масштабируемости, практический микро-бенчмарк сложности ($O(1)$ vs $O(N)$) и обязательный замок `microCheck` с одним проверочным вопросом.
```
