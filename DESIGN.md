# DESIGN.md — Python Backend Academy Design System & UI Specification

> **Standard**: Open-Source `DESIGN.md` Specification for AI UI Generators & Google Stitch  
> **Product**: Python Backend Academy (Interactive Micro-Learning Platform)  
> **Aesthetic Theme**: Evening Obsidian (*Dark Obsidian Glassmorphism*) & Morning Silk (*Clean Light Mode*)  
> **Primary Viewport**: Mobile Portrait `393×873px` (Xiaomi Mi 10T Pro / modern Android & iOS 390px) + Desktop `1440×900px`  
> **Core UX Philosophy**: Zero-Lag, Zero-Layout-Shift, Active Microlearning, Single Dominant CTA, Socratic Scaffolding.

---

## 1. Product Overview & Design Philosophy

Python Backend Academy is an interactive mastery-learning platform for aspiring Junior/Middle Python backend engineers. The user interface prioritizes extreme cognitive focus, visual serenity, and tactile feedback.

### Key Principles:
* **Evening Obsidian Aesthetic**: Deep cosmic obsidian background (`#080B10` to `#0F172A`) that reduces ocular fatigue during late-night coding sessions.
* **Atmospheric Glassmorphism**: Delicate translucent surfaces with hardware-accelerated blur (`backdrop-filter: blur(18px)`), micro-fine specular borders, and diffuse levitation drop shadows.
* **Ambient Lighting Discipline**: Strictly **two** subtle blurred glow orbs per screen (Emerald `#10B981` at top-left, Rose `#F43F5E` at bottom-right, `filter: blur(64px-72px)`) to keep 144Hz mobile rendering buttery-smooth.
* **Single Dominant CTA**: Every screen presents exactly **one** primary forward action to eliminate decision fatigue.
* **Zero Horizontal Scroll**: All code snippets, tables, and stepped paths are strictly constrained to avoid horizontal dragging on mobile displays.

---

## 2. Color Palette & Design Tokens

### 2.1. Dark Theme ("Evening Obsidian" — Primary)
* **Background Canvas**: `#080B10` (Ultra-deep obsidian black)
* **Surface Background**: `#0F172A` / `rgba(15, 23, 42, 0.60)` (Slate glass panel)
* **Surface Border**: `1px solid rgba(255, 255, 255, 0.12)`
* **Surface Inset Highlight**: `inset 0 1px 0 rgba(255, 255, 255, 0.18)`
* **Surface Elevation Shadow**: `0 16px 36px rgba(0, 0, 0, 0.45)`
* **Primary Text**: `#F8FAFC` (Slate 50, crisp white)
* **Secondary / Muted Text**: `#94A3B8` (Slate 400)
* **Subtle Borders / Dividers**: `rgba(255, 255, 255, 0.08)`

### 2.2. Light Theme ("Morning Silk" — Secondary Mirror)
* **Background Canvas**: `#F8FAFC`
* **Surface Background**: `rgba(255, 255, 255, 0.85)`
* **Surface Border**: `1px solid rgba(0, 0, 0, 0.08)`
* **Surface Elevation Shadow**: `0 10px 30px -10px rgba(15, 23, 42, 0.08)`
* **Primary Text**: `#0F172A`
* **Secondary Text**: `#64748B`

### 2.3. Semantic Accent Colors
* **Mastery Emerald**: `#10B981` (Success, mastered concepts, primary forward action CTA)
  * Dark Surface: `rgba(6, 78, 59, 0.28)`, Border: `#10B981`, Glow: `rgba(16, 185, 129, 0.18)`
* **Warm Amber**: `#F59E0B` (Streaks 🔥, XP badges, Socratic hints, hard cards)
  * Dark Surface: `rgba(180, 83, 9, 0.28)`, Border: `#F59E0B`, Glow: `rgba(245, 158, 11, 0.15)`
* **Vivid Rose**: `#F43F5E` (Errors, test failures, reset / "Don't know" cards)
  * Dark Surface: `rgba(136, 19, 55, 0.28)`, Border: `#F43F5E`, Glow: `rgba(244, 63, 94, 0.15)`
* **Electric Cyan**: `#06B6D4` (Active steps, interactive chips, easy review rating)
  * Dark Surface: `rgba(14, 116, 144, 0.28)`, Border: `#06B6D4`, Glow: `rgba(6, 182, 212, 0.18)`

---

## 3. Typography Scale & Fonts

* **Interface & Body Typography**: `Onest` (fallback: `Inter`, system-ui, sans-serif)
  * Clean modern geometric neo-grotesque with balanced Cyrillic/Latin geometry.
* **Code & Monospace Typography**: `JetBrains Mono` (fallback: `Fira Code`, monospace)
  * Used for code snippets, `<kbd>` shortcuts, terminal output, and numeric metrics.

| Level | Font Family | Weight | Size | Line Height | Tracking | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **H1** | `Onest` | Bold (700) | `24–28px` | `1.2` | `-0.02em` | Module & Screen titles |
| **H2** | `Onest` | Bold (700) | `18–20px` | `1.3` | `-0.015em` | Lesson cards, section headings |
| **Body** | `Onest` | Regular (400) | `14–15px` | `1.65` | `normal` | Study notes, conceptual descriptions |
| **Gamification Metric** | `Onest` | Black (900) | `24–32px` | `1.0` | `tight` | Streak count, total XP, mastery score |
| **Code Snippet** | `JetBrains Mono` | Medium (500) | `12–13px` | `1.5` | `normal` | Code editor, AST diff, terminal lines |
| **Micro-Badge / `<kbd>`** | `JetBrains Mono` | Bold (700) | `11px` | `1.0` | `+0.02em` | Keyboard hints, status pills (minimum 11px) |

---

## 4. Spacing, Elevation & Concentric Radii

### Concentric Corner Radii Scale:
Applied using the concentric containment formula $R_{\text{ext}} = R_{\text{int}} + \text{padding}$:
* `--r-xs: 4px` — `<kbd>` keycaps, language tag badges.
* `--r-sm: 8px` — Status pills, streak badges, tooltip cards.
* `--r-md: 14px` — **Action Buttons**, input text fields, SRS rating cards.
* `--r-lg: 20px` — Lesson summary cards, flashcard containers, Zen IDE split panels.
* `--r-xl: 28px` — Screen hero containers, exam milestone modals, dashboard focus card.

### Spacing Grid:
Based on a `4px / 8px` fluid modular grid: `4px`, `8px`, `12px`, `16px`, `20px`, `24px`, `32px`.

---

## 5. Canonical Component Specifications

### 5.1. SRS 4-Tier Flashcard Rating Buttons
A horizontal grid of 4 specialized rating buttons with `14px` border-radius and 2-line vertical label stack:
1. **Don't Know (Не знаю)**:
   * Label: `Не знаю` | Subtitle: `С нуля · [1]`
   * Color: Rose (`#F43F5E`) on Dark Wine background (`rgba(136, 19, 55, 0.28)`)
2. **Hard (Трудно)**:
   * Label: `Трудно (+2 XP)` | Subtitle: `1 дн · [2]`
   * Color: Warm Amber (`#F59E0B`) on Dark Amber background (`rgba(180, 83, 9, 0.28)`)
3. **Good (Хорошо)** — *The Benchmark Reference*:
   * Label: `Хорошо (+5 XP)` | Subtitle: `3 дн · [3]`
   * Color: Emerald (`#10B981`) on Dark Emerald background (`rgba(6, 78, 59, 0.28)`)
4. **Easy (Легко)**:
   * Label: `Легко (+10 XP)` | Subtitle: `7 дн · [4]`
   * Color: Electric Cyan (`#06B6D4`) on Dark Cyan background (`rgba(14, 116, 144, 0.28)`)

### 5.2. Bead Stepper Ribbon (Micro-Learning Progress)
Positioned strictly in a single-line card footer:
* **Left**: Current step indicator (e.g., `Шаг 3 из 12`, 13px Onest Medium).
* **Center**: Centered horizontal row of circular progress dots (`8px` diameter, active dot `10px` with emerald glow). Displays a 7-dot sliding window with subtle edge opacity fade.
* **Right**: Forward navigation button (`Дальше ➔`, 14px radius).

### 5.3. Zen IDE & Socratic Error Diff View
When unit tests fail, system tracebacks are replaced by a structured Socratic Diff Card:
* **Header**: Red cross icon `✗` + label `Расхождение с эталоном автотеста` + right-aligned button `💡 Взять наводку Сократа (1/4)`.
* **Student Output**: `- Ваш код: [1, 2, 3]` (Rose background with 3px solid border-left).
* **Expected Output**: `+ Ожидалось: [3, 2, 1]` (Emerald background with 3px solid border-left).

### 5.4. Single Dominant CTA Button
* Full-width or elevated central button with emerald gradient (`linear-gradient(135deg, #10B981, #059669)`).
* Corner radius: `14px`.
* Height: `48px` (mobile touch-friendly).
* Animated subtle specular sweep (*Shimmer Sweep*) across the button face.

### 5.5. Zen Rest Screen (`#/cards` Empty State)
When daily due cards reach zero (`cardsDueRemaining === 0`):
* Centered meditative icon `🧘`.
* Heading: `Очередь повторений чиста` (20px Onest Bold).
* Subheading: `Все карточки на сегодня закреплены в долговременной памяти. Время для нового материала на Тропе!`.
* Daily stats pills: Cards reviewed count, XP earned, current streak.
* Single Dominant CTA: `К СЛЕДУЮЩЕМУ УРОКУ НА ТРОПЕ ➔` (`#/path`).

### 5.6. Sticky Problem Anchor
* Top IDE banner displaying task signature (`def solution(...)`).
* Idle state: `38px` height with a `💡 Условие` toggle button.
* Keyboard focus state: Smoothly collapses to **`24px`** height (11px font), reclaiming 30% screen space for code input.

---

## 6. Motion & Audio Standards

### Motion Curves:
* **Spring Interactive** (Buttons, Cards, Badges):
  ```css
  transition: all 0.28s cubic-bezier(0.34, 1.56, 0.64, 1);
  ```
  Tap compression: `transform: scale(0.97);` on `:active`.
* **Snappy Reveal** (Drawers, Modals, Tooltips):
  ```css
  transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
  ```
* **Accessibility**: All keyframe animations disabled when `@media (prefers-reduced-motion: reduce)` is set.

### Sound Micro-Haptics (Web Audio API, 0 KB external files):
* **Card Flip / Review Grade**: 45ms sine sweep (800Hz $\to$ 400Hz, gentle exponential decay).
* **Success / Task Solved**: 220ms warm major triad chord (E5–G#5–B5).
* Mute toggle available in the top bar.

---

## 7. Mobile Usability & Viewport Rules

* **Device calibration**: Xiaomi Mi 10T Pro (`393×873px`, 20:9 ratio) & iPhone 13/14 (`390×844px`).
* **Zero Horizontal Code Overflow**:
  * Python code line lengths: Strictly **35–42 characters** (hard max 46 characters).
  * Trailing comments are strictly forbidden; comments are placed **above** the code line.
* **Touch Targets**: All interactive elements are minimum **`44×44px`**.
* **iOS Zoom Guard**: Text input elements declare `font-size: 16px` to prevent automatic screen zoom.
* **Safe Area Insets**: Handled via `padding-bottom: max(16px, env(safe-area-inset-bottom))`.

---

## 8. Content Tone & Didactic Invariants

1. **Human Language Only**: No machine nomenclature in the UI (no `K-001`, `F-001`, `Unit 1.1`, or raw UUIDs).
2. **Naming Restrictions**: The names "Coddy" / "Кодди" and the term "3D" are strictly forbidden.
3. **No Meta-Labels**: No labels like `Mental Model:` or `Pedagogical Objective:` in headers. Content dives directly into engineering phenomena.
4. **Stream Separation**:
   * `#/cards` — Pure daily due flashcard stream (SRS reviews).
   * `#/notes-review` — Dedicated Ebbinghaus study notes spaced repetition screen.
