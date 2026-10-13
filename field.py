from random import choice
from direction import Direction


class Field:
    def __init__(self, size: int) -> None:
        if size < 1:
            raise ValueError('Размер поля должен быть больше нуля')
        self.size = size
        self.grid: list[list[Direction | None]] = [
            [None] * self.size for _ in range(self.size)
            ]
        self._generate_field()
        self.remaining = self.size ** 2


    def _generate_field(self) -> None:
        mid = (self.size - 1) / 2

        for i in range(self.size):
            if i < mid:
                vertical_direction = [Direction.UP]
            elif i > mid:
                vertical_direction = [Direction.DOWN]
            else:
                vertical_direction = [Direction.UP, Direction.DOWN]
            
            for j in range(self.size):
                if j < mid:
                    horizontal_direction = [Direction.LEFT]
                elif j > mid:
                    horizontal_direction = [Direction.RIGHT]
                else:
                    horizontal_direction = [Direction.LEFT, Direction.RIGHT]
                
                self.grid[i][j] = choice(
                    vertical_direction + horizontal_direction
                    )


    def path_is_clear(
            self, cell: tuple[int, int], direction: Direction
            ) -> bool:
        row, col = direction.apply(cell)
        
        while 0 <= row < self.size and 0 <= col < self.size:
            if self.grid[row][col] is not None:
                return False
            
            row, col = direction.apply((row, col))
        
        return True

    
    def is_empty(self) -> bool:
        return self.remaining == 0


    def make_move(
            self, row: int, col: int, direction: Direction
            ) -> tuple[bool, str]:
        row_index, col_index = row - 1, col - 1

        if not (0 <= row_index < self.size and 0 <= col_index < self.size):
            return False, f'Такой клетки нет (допустимо 1..{self.size})'

        cell = self.grid[row_index][col_index]

        if cell is None:
            return False, 'В этой клетке нет стрелки'
        if cell != direction:
            return (
                False, 
                f'Неверное направление, '
                f'для клетки допустимо: {cell.name.lower()}.'
                )
        if not self.path_is_clear((row_index, col_index), direction):
            return False, 'Стрелка заблокирована'
        
        self.grid[row_index][col_index] = None
        self.remaining -= 1
        return True, 'Стрелка ушла!'


    def __str__(self) -> str:
        col_width = len(str(self.size)) + 4
        field: list[str] = []

        header = ' ' * col_width + ''.join(
            f'{i:^{col_width}}' for i in range(1, self.size + 1)
            )
        field.append(header)

        for row_idx, row in enumerate(self.grid, start=1):
            row_symbols = ''.join(
                f'{cell.symbol if cell is not None else "·":^{col_width}}' 
                for cell in row
                )

            field.append(f'{row_idx:^{col_width}}{row_symbols}')

        return '\n'.join(field)
