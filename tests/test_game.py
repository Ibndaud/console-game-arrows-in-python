"""Тесты логики «Стрелок»: поле, ходы, чистая resolve_click и жизненный цикл Game.

Запуск:  uv run pytest -q
Все тесты работают в headless-режиме (SDL_VIDEODRIVER=dummy из conftest.py).
"""
import random
import sys
from pathlib import Path

import pygame

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from direction import Direction  # noqa: E402
from field import Field  # noqa: E402
from game import (  # noqa: E402
    ERROR_COLOR,
    SUCCESS_COLOR,
    STATE_GAME_OVER,
    STATE_INPUT,
    STATE_PLAYING,
    Game,
    resolve_click,
)
from ui import TextInput  # noqa: E402

SUCCESS = SUCCESS_COLOR  # (30, 150, 70)
ERROR = ERROR_COLOR      # (200, 60, 60)


# ----------------------------------------------------------------------
# Поле: генерация и правила
# ----------------------------------------------------------------------
def solve(field: Field, budget: int = 50_000) -> bool:
    """Бэктрекинг: снимает первую доступную стрелку, откатываясь при тупиках."""
    state = {"budget": budget}

    def bt(remaining: int) -> bool:
        if state["budget"] <= 0:
            return False
        if remaining == 0:
            return True
        for r in range(field.size):
            for c in range(field.size):
                d = field.grid[r][c]
                if d is None:
                    continue
                ok, _ = field.make_move(r + 1, c + 1, d)
                if ok:
                    state["budget"] -= 1
                    if bt(remaining - 1):
                        return True
                    field.grid[r][c] = d
                    field.remaining += 1
        return False

    return bt(field.remaining)


def test_generated_fields_are_solvable():
    """Генератор обязан создавать только решаемые расстановки."""
    random.seed(42)
    for trial in range(30):
        size = 1 + trial % 5
        field = Field(size)
        assert field.remaining == size * size
        assert solve(field), f"поле {size}x{size} (попытка {trial}) не решается"


def test_make_move_validates_input():
    field = Field(3)

    ok, msg = field.make_move(0, 1, Direction.UP)
    assert not ok and 'клетки нет' in msg

    field.grid[1][1] = None
    field.remaining -= 1
    ok, msg = field.make_move(2, 2, Direction.UP)
    assert not ok and 'нет стрелки' in msg


def test_make_move_requires_matching_direction():
    field = Field(1)
    field.grid[0][0] = Direction.UP
    ok, msg = field.make_move(1, 1, Direction.LEFT)
    assert not ok and 'допустимо' in msg
    assert field.remaining == 1, "стрелка не должна сниматься"


def test_make_move_blocked_path_and_unblocking():
    field = Field(3)
    for c in range(3):
        field.grid[0][c] = Direction.RIGHT
    field.remaining = 3

    # левую и среднюю стрелки блокируют те, что стоят правее на их пути
    ok, msg = field.make_move(1, 1, Direction.RIGHT)
    assert not ok and 'заблокирована' in msg
    ok, msg = field.make_move(1, 2, Direction.RIGHT)
    assert not ok and 'заблокирована' in msg

    # правой стрелке путь свободен до края поля
    ok, msg = field.make_move(1, 3, Direction.RIGHT)
    assert ok and 'ушла' in msg

    # снятие правой разблокировало среднюю
    ok, msg = field.make_move(1, 2, Direction.RIGHT)
    assert ok


def test_path_is_clear_ray_semantics():
    field = Field(3)
    for c in range(3):
        field.grid[0][c] = Direction.RIGHT
    assert not field.path_is_clear((0, 1), Direction.RIGHT)  # (0, 2) занята
    assert field.path_is_clear((0, 2), Direction.RIGHT)      # дальше — край


# ----------------------------------------------------------------------
# Чистая игровая логика
# ----------------------------------------------------------------------
def test_resolve_click_messages():
    game = Game()
    game.text_input.text = '3'
    game._submit_size()

    game.field.grid[0][0] = None
    game.field.remaining -= 1
    assert resolve_click(game.field, 0, 0) == ('В этой клетке нет стрелки', ERROR)


def test_resolve_click_success_and_finish():
    game = Game()
    game.text_input.text = '1'
    game._submit_size()

    # resolve_click сам снимает единственную стрелку — поле пустеет
    _, color = resolve_click(game.field, 0, 0)
    assert color == SUCCESS
    assert game.field.is_empty()
    assert resolve_click(game.field, 0, 0) is None  # поле пустое — реакции нет


# ----------------------------------------------------------------------
# Ввод размера (TextInput)
# ----------------------------------------------------------------------
def key_event(key_name: str | None = None, unicode: str = '') -> pygame.event.Event:
    """KEYDOWN-событие; для «не клавишных» символов — K_UNKNOWN (важен только unicode)."""
    key = (
        getattr(pygame, f'K_{key_name.upper()}', pygame.K_UNKNOWN)
        if key_name else pygame.K_UNKNOWN
        )
    return pygame.event.Event(pygame.KEYDOWN, key=key, unicode=unicode)


def test_text_input_filters_digits():
    rect = pygame.Rect(0, 0, 120, 44)
    font = pygame.font.SysFont('Arial', 24)
    ti = TextInput(rect, font, max_length=2)

    for ch in '27a9.б':
        ti.handle_key(key_event(unicode=ch))
    assert ti.text == '27', "буквы и точки игнорируются, лимит — 2 цифры"

    ti.handle_key(key_event('backspace'))
    assert ti.text == '2'

    assert ti.handle_key(key_event('return')) == 'submit'


# ----------------------------------------------------------------------
# Полный жизненный цикл Game (headless)
# ----------------------------------------------------------------------
def test_game_lifecycle_input_play_gameover_restart():
    game = Game()
    assert game.state == STATE_INPUT

    # валидация ввода
    game.text_input.text = ''
    game._submit_size()
    assert game.input_error == 'Введите число'
    game.text_input.text = '99'
    game._submit_size()
    assert 'Допустимо' in game.input_error

    # старт игры
    game.text_input.text = '4'
    game._submit_size()
    assert game.state == STATE_PLAYING and game.field.size == 4

    # играем настоящими кликами до победы
    def click(row, col):
        m, cs = game.renderer.margin, game.renderer.cell_size
        game.handle_click((m + col * cs + cs // 2, m + row * cs + cs // 2))

    moves = 0
    while not game.field.is_empty():
        progressed = False
        for r in range(game.field.size):
            for c in range(game.field.size):
                d = game.field.grid[r][c]
                if d is not None and game.field.path_is_clear((r, c), d):
                    click(r, c)
                    moves += 1
                    progressed = True
                    break
            if progressed:
                break
        assert progressed, "нет доступных ходов"
        assert moves < 100, "слишком много ходов — похоже на бесконечный цикл"

    assert game.state == STATE_GAME_OVER
    assert moves == 16  # поле 4x4

    # рестарт с новым размером после победы
    game.text_input.text = '2'
    game._submit_size()
    assert game.state == STATE_PLAYING and game.field.size == 2
