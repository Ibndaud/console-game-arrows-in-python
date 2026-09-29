from random import choice


def create_field(size):
    return [[None]  * size for _ in range(size)]


def generate_field(size):
    field = create_field(size)
    for i in range(size):
        for j in range(size):
            if i < size // 2 and j < size // 2:
                field[i][j] = choice(('up', 'left'))
            elif i < size // 2:
                field[i][j] = choice(('up', 'right'))
            elif i >= size // 2 and j < size // 2:
                field[i][j] = choice(('down', 'left'))
            else:
                field[i][j] = choice(('down', 'right'))
    return field


def draw_field(grid):
    size = len(grid)
    col_width = len(str(size)) + 4
    print(' ' * col_width + ''.join(f'{i:^{col_width}}' for i in range(1, size + 1)))
    for row_idx in range(1, size + 1):
        row_symbols = [f'{SYMBOLS.get(cell):^{col_width}}' if cell else f'{"\u00B7":^{col_width}}' for cell in grid[row_idx - 1]]
        print(f'{row_idx:^{col_width}}' + ''.join(row_symbols))


def path_is_clear(grid, row, col, direction):
    size = len(grid)
    dr, dc = DIRECTIONS[direction]
    row, col = row + dr, col + dc
    while 0 <= row < size and 0 <= col < size:
        if grid[row][col] is not None:
            return False
        row, col = row + dr, col + dc
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
    return not any(cell for row in grid for cell in row)


def game_cycle(grid):
    while True:
        draw_field(grid)
        try:
            row, col, direction = input().split()
            row, col, direction = int(row), int(col), direction.lower()
            if direction not in DIRECTIONS:
                print('Неизвестное направление')
                continue
            break
        except ValueError:
            print('Неверный формат ввода')
    make_move(grid, row, col, direction)
    
    
def get_size():
    user_input = None
    while user_input is None:
        user_input = input()
        try:
            user_input = int(user_input)
        except ValueError:
            user_input = None
            print('Введите целое число')
            continue
        if user_input < 1:
            user_input = None
            print('Размер поля должен быть больше нуля')
    return user_input


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
    game_cycle(grid)

print('Игра окончена!')