import pygame
import sys

from field import Field
from ui import FieldRenderer


FPS = 60
MAX_SCREEN_WIDTH = 800
MAX_SCREEN_HEIGHT = 800
MARGIN = 40
MESSAGE_AREA_HEIGHT = 80
MESSAGE_Y_OFFSET = 60
REMAINING_Y_OFFSET = 100

BACKGROUND = (235, 240, 245)
TEXT_COLOR = (30, 30, 30)
SUCCESS_COLOR = (30, 150, 70)
ERROR_COLOR = (200, 60, 60)

DEFAULT_MESSAGE = 'Нажмите на стрелку, R - перезапустить игру'


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

    if success and field.is_empty():
        return 'Игра окончена!', SUCCESS_COLOR
    if success:
        return message, SUCCESS_COLOR
    return message, ERROR_COLOR


class Game:
    def __init__(self, size: int) -> None:
        pygame.init()

        self.field = Field(size)
        self.cell_size = min(
            (MAX_SCREEN_WIDTH - MARGIN * 2) // size,
            (MAX_SCREEN_HEIGHT - MARGIN * 2 - MESSAGE_AREA_HEIGHT) // size
            )
        self.renderer = FieldRenderer(
            self.field, self.cell_size, margin=MARGIN
            )
        self.screen_width = (self.renderer.grid_size + MARGIN * 2)
        self.screen_height = (
            self.renderer.grid_size + MARGIN * 2 + MESSAGE_AREA_HEIGHT
            )
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
            )
        pygame.display.set_caption('Arrow Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.running = True
        self._set_message(DEFAULT_MESSAGE, TEXT_COLOR)


    def handle_events(self) -> None:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.handle_click(event.pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()


    def handle_click(self, mouse_pos: tuple[int, int]) -> None:
        cell = self.renderer.get_cell_at(mouse_pos)

        if cell is None:
            return

        row, col = cell
        result = resolve_click(self.field, row, col)

        if result is not None:
            self._set_message(*result)


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
        hovered_cell = self.renderer.get_cell_at(pygame.mouse.get_pos())
        self.renderer.draw(self.screen, hovered_cell)

        self._draw_text(
            self.message, 
            self.message_color, 
            self.screen_height - MESSAGE_Y_OFFSET
            )
        self._draw_text(
            f'Осталось стрелок: {self.field.remaining}', 
            TEXT_COLOR,
            self.screen_height - REMAINING_Y_OFFSET
            )

        pygame.display.flip()


    def run(self) -> None:
        while True:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
            if not self.running:
                pygame.quit()
                sys.exit()


    def reset(self) -> None:
        self.field = Field(self.field.size)
        self.renderer.field = self.field
        self._set_message(DEFAULT_MESSAGE, TEXT_COLOR)
