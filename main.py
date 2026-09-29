from random import choice


def create_field():
    return [[None]  * SIZE for _ in range(SIZE)]


def generate_field():
    field = create_field()
    for i in range(SIZE):
        for j in range(SIZE):
            if i < SIZE // 2 and j < SIZE // 2:
                field[i][j] = choice(('up', 'left'))
            elif i < SIZE // 2:
                field[i][j] = choice(('up', 'right'))
            elif i >= SIZE // 2 and j < SIZE // 2:
                field[i][j] = choice(('down', 'left'))
            else:
                field[i][j] = choice(('down', 'right'))
    return field


def draw_field(grid):
    print('\t' + '\t'.join(map(str, range(1, SIZE + 1))))
    for row_idx in range(1, SIZE + 1):
        row_symbols = [SYMBOLS.get(cell) if cell else '\u00B7' for cell in grid[row_idx - 1]]
        print(str(row_idx) + '\t' + '\t'.join(row_symbols))


def path_is_clear(grid, row, col, direction):
    dr, dc = DIRECTIONS.get(direction)
    row, col = row + dr, col + dc
    while 0 <= row < SIZE and 0 <= col < SIZE:
        if grid[row][col]:
            return False
        row, col = row + dr, col + dc
    return True


def make_move(grid, row, col, direction):
    row_index, col_index = row - 1, col - 1
    if not (0 <= row_index < SIZE) or not (0 <= col_index < SIZE):
        print('Такой клетки нет')
        return
    if not grid[row_index][col_index]:
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
grid = generate_field()

while not is_empty(grid):
    game_cycle(grid)

print('Игра окончена!')