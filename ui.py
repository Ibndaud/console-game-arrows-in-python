from __future__ import annotations

import pygame

from direction import Direction

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from field import Field


# Цвета
BACKGROUND = (235, 240, 245)
CELL_COLOR = (255, 255, 255)
GRID_COLOR = (180, 190, 200)
ARROW_COLOR = (40, 80, 160)
HOVER_COLOR = (210, 230, 255)

TEXT_COLOR = (30, 30, 30)


class TextInput:
    """Простое однострочное поле ввода цифр для pygame-окна."""

    def __init__(
            self, rect: pygame.Rect, font: pygame.font.Font,
            max_length: int = 2
            ) -> None:
        self.rect = rect
        self.font = font
        self.text = ''
        self.max_length = max_length

    def handle_key(self, event: pygame.event.Event) -> str | None:
        """
        Обрабатывает KEYDOWN-событие.
        Возвращает 'submit', если нажат Enter, иначе None.
        """
        if event.key == pygame.K_RETURN:
            return 'submit'
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif event.unicode.isdigit() and len(self.text) < self.max_length:
            self.text += event.unicode
        return None

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, CELL_COLOR, self.rect)
        pygame.draw.rect(screen, GRID_COLOR, self.rect, 2)

        surface = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = surface.get_rect(
            midleft=(self.rect.x + 12, self.rect.centery)
            )
        screen.blit(surface, text_rect)

        cursor_x = text_rect.right + 2 if self.text else self.rect.x + 12
        if pygame.time.get_ticks() % 1000 < 500:
            pygame.draw.line(
                screen, TEXT_COLOR,
                (cursor_x, self.rect.y + 8), (cursor_x, self.rect.bottom - 8),
                2
                )



class FieldRenderer:
    def __init__(
            self, field: Field, cell_size: int = 60, margin: int = 40
            ) -> None:

        self.field = field
        self.cell_size = cell_size
        self.margin = margin
        self.grid_size = self.field.size * self.cell_size
        self.grid_rect = pygame.Rect(
            self.margin, self.margin, self.grid_size, self.grid_size
            )


    def draw(self, screen, hovered_cell=None):
        """Рисует поле: клетки, сетку, стрелки и подсветку клетки под курсором."""
        for row in range(self.field.size):
            for col in range(self.field.size):
                x = self.margin + col * self.cell_size
                y = self.margin + row * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                color = CELL_COLOR

                if hovered_cell == (row, col):
                    color = HOVER_COLOR

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)

                direction = self.field.grid[row][col]

                if direction is not None:
                    self.draw_arrow(screen, rect, direction)


    def get_cell_at(
            self, mouse_pos: tuple[int, int]
            ) -> tuple[int, int] | None:
        
        mouse_x, mouse_y = mouse_pos

        if not self.grid_rect.collidepoint(mouse_pos):
            return None

        col = (mouse_x - self.margin) // self.cell_size
        row = (mouse_y - self.margin) // self.cell_size

        return row, col


    def draw_arrow(
            self, 
            screen: pygame.Surface, 
            rect: pygame.Rect, 
            direction: Direction,
            ) -> None:
        cx, cy = rect.center

        # Размеры стрелки относительно клетки
        half_length = self.cell_size * 0.275
        head_length = self.cell_size * 0.18
        head_width = self.cell_size * 0.22
        line_width = max(2, int(self.cell_size * 0.06))

        # Единичный вектор направления в экранных координатах.
        # В Pygame X направлен вправо, Y — вниз.
        dx = direction.dc
        dy = direction.dr

        # Конец древка / кончик стрелки
        tip_x = cx + dx * half_length
        tip_y = cy + dy * half_length

        # Начало древка
        start_x = cx - dx * half_length
        start_y = cy - dy * half_length

        # Основание наконечника
        base_x = tip_x - dx * head_length
        base_y = tip_y - dy * head_length

        # Перпендикуляр к направлению
        perp_x = -dy
        perp_y = dx

        # Два угла основания треугольника
        p1 = (
            base_x + perp_x * head_width / 2, base_y + perp_y * head_width / 2,
            )
        p2 = (
            base_x - perp_x * head_width / 2, base_y - perp_y * head_width / 2,
            )

        # Древко
        pygame.draw.line(
            screen,
            ARROW_COLOR,
            (start_x, start_y),
            (base_x, base_y),
            line_width,
            )

        # Наконечник
        pygame.draw.polygon(
            screen,
            ARROW_COLOR,
            [(tip_x, tip_y), p1, p2],
            )