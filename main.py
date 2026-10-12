from random import choice
from direction import Direction


class Field:
    def __init__(self, size: int) -> None:
        self.size = size
        self.grid: list[list[Direction | None]] = [[None] * self.size for _ in range(self.size)]
        self._create_field()


    def _create_field(self) -> None:
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
                
                self.grid[i][j] = choice(vertical_direction + horizontal_direction)


    def path_is_clear(self, cell: tuple[int, int], direction: Direction) -> bool:
        row, col = direction.apply(cell)
        
        while 0 <= row < self.size and 0 <= col < self.size:
            if self.grid[row][col] is not None:
                return False
            
            row, col = direction.apply((row, col))
        
        return True

    
    def is_empty(self) -> bool:
        return all(cell is None for row in self.grid for cell in row)


    def make_move(self, row: int, col: int, direction: Direction) -> tuple[bool, str]:
        row_index, col_index = row - 1, col - 1

        if not (0 <= row_index < self.size and 0 <= col_index < self.size):
            return False, f'Такой клетки нет (допустимо 1..{self.size})'
        if self.grid[row_index][col_index] is None:
            return False, 'В этой клетке нет стрелки'
        if self.grid[row_index][col_index] != direction:
            return False, f'Неверное направление, для клетки допустимо: {self.grid[row_index][col_index].name.lower()}.'
        if not self.path_is_clear((row_index, col_index), direction):
            return False, 'Стрелка заблокирована'
        
        self.grid[row_index][col_index] = None
        return True, 'Стрелка ушла!'


    def draw(self) -> None:
        col_width = len(str(self.size)) + 4
        print(' ' * col_width + ''.join(f'{i:^{col_width}}' for i in range(1, self.size + 1)))

        for row_idx, row in enumerate(self.grid, start=1):
            row_symbols = ''.join(
                f'{cell.symbol if cell is not None else "\u00B7":^{col_width}}' 
                for cell in row
                )
            print(f'{row_idx:^{col_width}}{row_symbols}')


class Game:
    def __init__(self) -> None:
        self.field = Field(self.get_size())


    def run(self) -> None:
        while not self.field.is_empty():
            self.game_turn()

        print('Игра окончена!')


    def get_size(self) -> int:
        while True:
            try:
                size = int(input('Введите размер поля: '))
            except ValueError:
                print('Введите целое число')
                continue
            if size < 1:
                print('Размер поля должен быть больше нуля')
                continue
            return size


    def game_turn(self) -> None:
        while True:
            self.field.draw()
            try:
                row, col, direction = input('Введите номер строки, столбца и направление: ').split()
                row, col = int(row), int(col)
            except ValueError:
                print('Неверный формат ввода')
                continue
            
            try:
                direction = Direction.from_string(direction)
            except KeyError:
                valid = ', '.join(d.name.lower() for d in Direction)
                print(f'Неизвестное направление. Допустимо: {valid}.')
                continue

            _, message = self.field.make_move(row, col, direction)
            print(message)
            return


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()