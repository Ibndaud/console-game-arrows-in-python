import pygame

from direction import Direction
from field import Field


# Цвета
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)

BACKGROUND = (235, 240, 245)
CELL_COLOR = (255, 255, 255)
GRID_COLOR = (180, 190, 200)
ARROW_COLOR = (40, 80, 160)
HOVER_COLOR = (210, 230, 255)


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
        length = self.cell_size * 0.55
        head_length = self.cell_size * 0.18
        head_width = self.cell_size * 0.22
        line_width = max(2, int(self.cell_size * 0.06))

        # Единичный вектор направления в экранных координатах.
        # В Pygame X направлен вправо, Y — вниз.
        dx = direction.dc
        dy = direction.dr

        # Конец древка / кончик стрелки
        tip_x = cx + dx * length / 2
        tip_y = cy + dy * length / 2

        # Начало древка
        start_x = cx - dx * length / 2
        start_y = cy - dy * length / 2

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