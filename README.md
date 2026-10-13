# ➡️ «Стрелки» — головоломка на pygame

![CI](https://github.com/Ibndaud/console-game-arrows-in-python/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?logo=python&logoColor=white)
![pygame](https://img.shields.io/badge/pygame-2.6%2B-1E9B47?logo=python&logoColor=white)
![Code style](https://img.shields.io/badge/code%20style-ruff-261230)
![License](https://img.shields.io/badge/license-MIT-green)

Учебный проект с курса **[«Python: от стрелок до ООП»](https://stepik.org/course/297691)** (Людмила Колесникова, Stepik): головоломка «Стрелки», прошедшая путь от консольного прототипа в одном файле до GUI-игры на pygame с модульной архитектурой.

---

## 🎮 Правила

<p align="center">
  <img src="img/gameplay.gif" width="440" alt="Геймплей «Стрелок»: курсор наводится на стрелку, клик снимает её; стрелки исчезают одна за другой до полной очистки поля">
</p>

На поле N×N в каждой клетке — стрелка, указывающая в одну из четырёх сторон.

- **Снять стрелку можно, только если на её пути до края поля нет других стрелок**;
- цель — очистить поле полностью;
- генератор поля всегда создаёт **решаемую** расстановку (взаимные «блокировки» исключены конструкцией генерации от центра поля).

| Управление | Действие |
|---|---|
| **ЛКМ** по стрелке | снять (если путь свободен) |
| **R** | новая игра |

Подсказки под полем: счётчик оставшихся стрелок и сообщение о результате хода (зелёное — успех, красное — ошибка). Клетка под курсором подсвечивается.

<details>
<summary>Скриншот середины игры</summary>

![Поле 5×5 в середине игры: часть стрелок снята, осталось 12](img/gameplay.png)
</details>

---

## 🧠 Эволюция проекта

Проект сознательно сохраняет историю «как код становится программой» — три этапа:

| Этап | Файлы | Что появилось |
|---|---|---|
| 1. Консольный прототип | [`legacy/arrow_puzzle.py`](legacy/arrow_puzzle.py) | функции, глобальная `SIZE`, ввод `row col direction` из консоли |
| 2. Рефакторинг кода из курса + оптимизация | [`legacy/arrow_puzzle_fixed.py`](legacy/arrow_puzzle_fixed.py) | размер поля параметром, `mid = (size - 1) / 2` — генерация любых размеров |
| 3. Модульная версия + OOP + GUI | `direction.py`, `field.py`, `game.py`, `ui.py`, `main.py` | классы по ответственности, enum направлений, pygame-рендер |

Историю шагов подробно видно в коммитах: `added class Field` → `added enum - directions` → `refactored code in separated files` → `rewrited using pygame`.

## 📐 Как устроен код

| Модуль | Ответственность |
|---|---|
| `direction.py` | `Direction` — enum: вектор смещения `(dr, dc)`, юникод-символ, `apply(cell)` и парсинг `from_string()` |
| `field.py` | `Field` — состояние игры: генерация решаемого поля, `make_move()` с тремя проверками (клетка, направление, путь), рендер в текст для консоли |
| `ui.py` | `FieldRenderer` — pygame-отрисовка: сетка, hover-подсветка, стрелки геометрией (древко + наконечник считаются векторами направления) |
| `game.py` | `Game` — цикл событий, клики, сообщения, рестарт |
| `main.py` | точка входа: ввод размера поля с валидацией (1..30) |

**Нюансы реализации:**
- путь проверяется «лучом» от клетки до края — `path_is_clear()`;
- стрелки рисуются не шрифтом, а полигонами — масштабируются под любой размер клетки;
- консольная и GUI-версии делят одну и ту же логику `Field` — это и есть выгода от разделения ответственности.

---

## 🚀 Запуск

**Требования:** Python 3.13+, [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/Ibndaud/console-game-arrows-in-python.git
cd console-game-arrows-in-python

uv sync
uv run python main.py
```

<details>
<summary>Без uv (pip + venv)</summary>

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install pygame
python main.py
```
</details>

Размер поля вводится в консоли до открытия окна (по умолчанию допускается 1..30).

## 🛠 Разработка

```bash
uvx ruff check .     # те же проверки, что в CI
```

CI (`.github/workflows/ci.yml`): линтинг ruff + smoke-тесты (компиляция и headless-импорт модулей) на каждый push и pull request.

## 📄 Лицензия

[MIT](LICENSE)
