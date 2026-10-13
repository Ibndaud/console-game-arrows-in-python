import pygame
import sys

from field import Field
from ui import FieldRenderer, TextInput


FPS = 60
MAX_SCREEN_WIDTH = 800
MAX_SCREEN_HEIGHT = 800
MARGIN = 40
MESSAGE_AREA_HEIGHT = 80
MESSAGE_Y_OFFSET = 60
REMAINING_Y_OFFSET = 100
MIN_FIELD_SIZE = 1
MAX_FIELD_SIZE = 30

BACKGROUND = (235, 240, 245)
TEXT_COLOR = (30, 30, 30)
SUCCESS_COLOR = (30, 150, 70)
ERROR_COLOR = (200, 60, 60)

DEFAULT_MESSAGE = 'Нажмите на стрелку, R - перезапустить игру'

STATE_INPUT = 'input'
STATE_PLAYING = 'playing'
STATE_GAME_OVER = 'game_over'

SCREEN_TITLES = {
    STATE_INPUT: 'Размер поля',
    STATE_GAME_OVER: 'Игра окончена!',
}


def resolve_click(
        field: Field, row: int, col: int
        ) -> tuple[str, tuple[int, int, int]] | None:
    """
    Чистая игровая логика: по клику на клетку определяет текст
    и цвет сообщения. Не зависит от pygame и не трогает UI,
    поэтому легко тестируется без поднятия окна.

    Возвращает None, если реагировать не нужно (поле уже пустое).
    """
    if field.is_empty():
        return None

    direction = field.grid[row][col]

    if direction is None:
        return 'В этой клетке нет стрелки', ERROR_COLOR

    success, message = field.make_move(row + 1, col + 1, direction)

    if success:
        return message, SUCCESS_COLOR
    return message, ERROR_COLOR

class Game:
    def __init__(self) -> None:
    # def __init__(self, size: int) -> None:
        pygame.init()

        self.running = True
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 32, bold=True)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('Arrow Game')
        self._show_size_screen(STATE_INPUT)


    def _show_size_screen(self, state: str) -> None:
        self.state = state
        self.input_error = None

        self.screen_width = MAX_SCREEN_WIDTH
        self.screen_height = MAX_SCREEN_HEIGHT
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
            )

        input_rect = pygame.Rect(0, 0, 120, 44)
        input_rect.center = (self.screen_width // 2, self.screen_height // 2)
        self.text_input = TextInput(input_rect, self.font, max_length=2)


    def _handle_size_screen_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            result = self.text_input.handle_key(event)
            if result == 'submit':
                self._submit_size()


    def _submit_size(self) -> None:
        text = self.text_input.text

        if not text:
            self.input_error = 'Введите число'
            return

        size = int(text)

        if not (MIN_FIELD_SIZE <= size <= MAX_FIELD_SIZE):
            self.input_error = (
                f'Допустимо от {MIN_FIELD_SIZE} до {MAX_FIELD_SIZE}'
                )
            return

        self.start_game(size)


    def _draw_size_screen(self) -> None:
        title = SCREEN_TITLES[self.state]
        title_surface = self.title_font.render(title, True, TEXT_COLOR)
        title_rect = title_surface.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 - 70)
            )
        self.screen.blit(title_surface, title_rect)

        self.text_input.draw(self.screen)

        hint = f'Введите число от {MIN_FIELD_SIZE} до {MAX_FIELD_SIZE}, Enter — начать'
        self._draw_text(hint, TEXT_COLOR, self.screen_height // 2 + 60)

        if self.input_error:
            self._draw_text(
                self.input_error, ERROR_COLOR,
                self.screen_height // 2 + 90
                )


    def start_game(self, size: int) -> None:
        self.field = Field(size)
        self.cell_size = min(
            (MAX_SCREEN_WIDTH - MARGIN * 2) // size,
            (MAX_SCREEN_HEIGHT - MARGIN * 2 - MESSAGE_AREA_HEIGHT) // size
            )
        self.renderer = FieldRenderer(self.field, self.cell_size, margin=MARGIN)

        self.screen_width = self.renderer.grid_size + MARGIN * 2
        self.screen_height = (
            self.renderer.grid_size + MARGIN * 2 + MESSAGE_AREA_HEIGHT
            )
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
            )

        self.state = STATE_PLAYING
        self._set_message(DEFAULT_MESSAGE, TEXT_COLOR)


    def _handle_playing_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.start_game(self.field.size)


    def handle_events(self) -> None:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
                return

            if self.state in (STATE_INPUT, STATE_GAME_OVER):
                self._handle_size_screen_event(event)
            elif self.state == STATE_PLAYING:
                self._handle_playing_event(event)


    def handle_click(self, mouse_pos: tuple[int, int]) -> None:
        cell = self.renderer.get_cell_at(mouse_pos)

        if cell is None:
            return

        row, col = cell
        result = resolve_click(self.field, row, col)

        if result is None:
            return
        
        message, color = result
        self._set_message(message, color)

        if self.field.is_empty():
            self._end_game()


    def _end_game(self) -> None:
        self._show_size_screen(STATE_GAME_OVER)


    def _draw_playing_screen(self) -> None:
        hovered_cell = self.renderer.get_cell_at(pygame.mouse.get_pos())
        self.renderer.draw(self.screen, hovered_cell)

        self._draw_text(
            self.message, self.message_color,
            self.screen_height - MESSAGE_Y_OFFSET
            )
        self._draw_text(
            f'Осталось стрелок: {self.field.remaining}', TEXT_COLOR,
            self.screen_height - REMAINING_Y_OFFSET
            )


    def _set_message(self, text: str, color: tuple[int, int, int]) -> None:
        self.message, self.message_color = text, color


    def _draw_text(
            self, text: str, color: tuple[int, int, int], y: int
            ) -> None:
        surface = self.font.render(text, True, color)
        rect = surface.get_rect(center=(self.screen_width // 2, y))
        self.screen.blit(surface, rect)


    def draw(self) -> None:
        self.screen.fill(BACKGROUND)

        if self.state in (STATE_INPUT, STATE_GAME_OVER):
            self._draw_size_screen()
        elif self.state == STATE_PLAYING:
            self._draw_playing_screen()

        pygame.display.flip()


    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
        