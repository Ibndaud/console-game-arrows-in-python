import pygame
import sys

from field import Field
from ui import FieldRenderer
from direction import Direction


FPS = 60
MAX_SCREEN_WIDTH = 800
MAX_SCREEN_HEIGHT = 800
MARGIN = 40
MESSAGE_AREA_HEIGHT = 80

BACKGROUND = (235, 240, 245)
TEXT_COLOR = (30, 30, 30)
SUCCESS_COLOR = (30, 150, 70)
ERROR_COLOR = (200, 60, 60)


class Game:
    def __init__(self, size: int) -> None:
        pygame.init()

        self.field = Field(size)
        self.cell_size = min(
            (MAX_SCREEN_WIDTH - MARGIN * 2) // size,
            (MAX_SCREEN_HEIGHT - MARGIN * 2 - 100) // size
            )
        self.renderer = FieldRenderer(self.field, self.cell_size, margin=MARGIN)
        self.screen_width = (self.renderer.grid_size + MARGIN * 2)
        self.screen_height = (self.renderer.grid_size + MARGIN * 2 + MESSAGE_AREA_HEIGHT)
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
            )
        pygame.display.set_caption('Arrow Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.message = 'Нажмите на стрелку'
        self.message_color = TEXT_COLOR


    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.handle_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()


    def handle_click(self, mouse_pos):
        if self.field.is_empty():
            return
        
        cell = self.renderer.get_cell_at(mouse_pos)

        if cell is None:
            return

        row, col = cell
        direction = self.field.grid[row][col]

        if direction is None:
            self._set_message('В этой клетке нет стрелки', ERROR_COLOR)
            # self.message = 'В этой клетке нет стрелки'
            # self.message_color = ERROR_COLOR
            return

        success, message = self.field.make_move(row + 1, col + 1, direction)
        self.message = message

        if success and self.field.is_empty():
            self._set_message('Игра окончена!', SUCCESS_COLOR)
            # self.message = 'Игра окончена!'
            # self.message_color = SUCCESS_COLOR
        elif success:
            self.message_color = SUCCESS_COLOR
        else:
            self.message_color = ERROR_COLOR


    def _set_message(self, text, color):
        self.message, self.message_color = text, color


    def draw(self):
        self.screen.fill(BACKGROUND)
        hovered_cell = self.renderer.get_cell_at(pygame.mouse.get_pos())
        self.renderer.draw(self.screen, hovered_cell)
        message_surface = self.font.render(
            self.message, True, self.message_color
            )
        message_rect = message_surface.get_rect(
            center=(self.screen_width // 2, self.screen_height - 60)
            )
        self.screen.blit(message_surface, message_rect)
        remaining_text = self.font.render(
            f'Осталось стрелок: {self.field.remaining}', True, TEXT_COLOR
            )
        remaining_rect = remaining_text.get_rect(
            center=(self.screen_width // 2, self.screen_height - 100)
            )
        self.screen.blit(remaining_text, remaining_rect)
        pygame.display.flip()


    def run(self):
        while True:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)


    def reset(self):
        self.field = Field(self.field.size)
        self.renderer.field = self.field

        self._set_message('Нажмите на стрелку', TEXT_COLOR)
        # self.message = 'Нажмите на стрелку'
        # self.message_color = TEXT_COLOR


# # консольный вариант класса
# class Game:
#     def __init__(self, size: int) -> None:
#         self.field = Field(size)


#     def run(self) -> None:
#         while not self.field.is_empty():
#             self.game_turn()

#         print('Игра окончена!')


#     def game_turn(self) -> None:
#         while True:
#             print(self.field)
#             try:
#                 row, col, direction = input(
#                     'Введите номер строки, столбца и направление: '
#                     ).split()
#                 row, col = int(row), int(col)
#             except ValueError:
#                 print('Неверный формат ввода')
#                 continue
            
#             try:
#                 direction = Direction.from_string(direction)
#             except KeyError:
#                 valid = ', '.join(d.name.lower() for d in Direction)
#                 print(f'Неизвестное направление. Допустимо: {valid}.')
#                 continue

#             _, message = self.field.make_move(row, col, direction)
#             print(message)
#             return
