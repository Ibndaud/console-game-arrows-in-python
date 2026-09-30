from random import choice


def create_field(size):
    return [[None]  * size for _ in range(size)]


def generate_field(size):
    field = create_field(size)
    mid = (size - 1) / 2
    
    for i in range(size):
        if i < mid:
            vertical_direction = ['up']
        elif i > mid:
            vertical_direction = ['down']
        else:
            vertical_direction = ['up', 'down']
        
        for j in range(size):
            if j < mid:
                horizontal_direction = ['left']
            elif j > mid:
                horizontal_direction = ['right']
            else:
                horizontal_direction = ['left', 'right']
            
            field[i][j] = choice(vertical_direction + horizontal_direction)
    
    return field


def draw_field(grid):
    size = len(grid)
    col_width = len(str(size)) + 4

    print(' ' * col_width + ''.join(f'{i:^{col_width}}' for i in range(1, size + 1)))

    for row_idx, row in enumerate(grid, start=1):
        row_symbols = ''.join(
            f'{SYMBOLS[cell] if cell else "\u00B7":^{col_width}}' 
            for cell in row
            )
        
        print(f'{row_idx:^{col_width}}{row_symbols}')


def path_is_clear(grid, row, col, direction):
    size = len(grid)
    dr, dc = DIRECTIONS[direction]

    row += dr
    col += dc
    
    while 0 <= row < size and 0 <= col < size:
        if grid[row][col] is not None:
            return False
        
        row += dr
        col += dc
    
    return True


def make_move(grid, row, col, direction):
    size = len(grid)
    row_index, col_index = row - 1, col - 1
    if not (0 <= row_index < size and 0 <= col_index < size):
        print('Такой клетки нет')
        return
    if grid[row_index][col_index] is None:
        print('В этой клетке нет стрелки')
        return
    if grid[row_index][col_index] != direction:
        print('Неверное направление')
        return
    if not path_is_clear(grid, row_index, col_index, direction):
        print('Стрелка заблокирована')
        return
    grid[row_index][col_index] = None
    print('Стрелка ушла!')

    
def is_empty(grid):
    return all(cell is None for row in grid for cell in row)


def game_turn(grid):
    while True:
        draw_field(grid)
        try:
            row, col, direction = input('Введите номер строки, столбца и направление: ').split()
            row, col, direction = int(row), int(col), direction.lower()
        except ValueError:
            print('Неверный формат ввода')
            continue

        if direction not in DIRECTIONS:
            print('Неизвестное направление')
            continue

        make_move(grid, row, col, direction)
        return
    

def get_size():
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

SIZE = get_size()
grid = generate_field(SIZE)

while not is_empty(grid):
    game_turn(grid)

print('Игра окончена!')