from random import choice


SYMBOLS = {
    'left': '←',
    'right': '→',
    'up': '↑',
    'down': '↓'
}
DIRECTIONS = {
    'left': (0, -1),
    'right': (0, 1),
    'up': (-1, 0),
    'down': (1, 0)
}


class Field:
    def __init__(self, size: int):
        self.size = size
        self.grid = [[None] * self.size for _ in range(self.size)]
        self._create_field()


    def _create_field(self):
        mid = (self.size - 1) / 2

        for i in range(self.size):
            if i < mid:
                vertical_direction = ['up']
            elif i > mid:
                vertical_direction = ['down']
            else:
                vertical_direction = ['up', 'down']
            
            for j in range(self.size):
                if j < mid:
                    horizontal_direction = ['left']
                elif j > mid:
                    horizontal_direction = ['right']
                else:
                    horizontal_direction = ['left', 'right']
                
                self.grid[i][j] = choice(vertical_direction + horizontal_direction)


    def path_is_clear(self, row, col, direction):
        dr, dc = DIRECTIONS[direction]
        
        row += dr
        col += dc
        
        while 0 <= row < self.size and 0 <= col < self.size:
            if self.grid[row][col] is not None:
                return False
            
            row += dr
            col += dc
        
        return True

    
    def is_empty(self):
        return all(cell is None for row in self.grid for cell in row)


    def make_move(self, row, col, direction):
        row_index, col_index = row - 1, col - 1

        if not (0 <= row_index < self.size and 0 <= col_index < self.size):
            return False, 'Такой клетки нет'
        if self.grid[row_index][col_index] is None:
            return False, 'В этой клетке нет стрелки'
        if self.grid[row_index][col_index] != direction:
            return False, 'Неверное направление'
        if not self.path_is_clear(row_index, col_index, direction):
            return False, 'Стрелка заблокирована'
        
        self.grid[row_index][col_index] = None
        return True, 'Стрелка ушла!'


    def draw(self):
        col_width = len(str(self.size)) + 4
        print(' ' * col_width + ''.join(f'{i:^{col_width}}' for i in range(1, self.size + 1)))

        for row_idx, row in enumerate(self.grid, start=1):
            row_symbols = ''.join(
                f'{SYMBOLS[cell] if cell is not None else "\u00B7":^{col_width}}' 
                for cell in row
                )
            print(f'{row_idx:^{col_width}}{row_symbols}')


class Game:
    def __init__(self):
        self.field = None


    def run(self):
        self.field = Field(self.get_size())

        while not self.field.is_empty():
            self.game_turn()

        print('Игра окончена!')


    def get_size(self):
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


    def game_turn(self):
        while True:
            self.field.draw()
            try:
                row, col, direction = input('Введите номер строки, столбца и направление: ').split()
                row, col, direction = int(row), int(col), direction.lower()
            except ValueError:
                print('Неверный формат ввода')
                continue
            
            if direction not in DIRECTIONS:
                print('Неизвестное направление')
                continue

            result, message = self.field.make_move(row, col, direction)
            print(message)
            return

        





def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()