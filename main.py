from random import choice


def create_field():
    return [[None]  * SIZE for i in range(SIZE)]


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
    for i in range(SIZE + 1):
        if not i:
            print('\t' + '\t'.join(map(str, range(1, SIZE + 1))))
            continue
        print(str(i) + '\t' + '\t'.join([SYMBOLS.get(i) if i else '\u00B7' for i in grid[i - 1]]))


def path_is_clear(grid, row, col, direction):
    dr, dc = DIRECTIONS.get(direction)
    row, col = row + dr, col + dc
    while row >= 0 and row < SIZE and col >= 0 and col < SIZE:
        if grid[row][col]:
            return False
        row, col = row + dr, col + dc
    return True


def make_move(grid, row, col, direction):
    x, y = row - 1, col - 1
    if not (0 <= x < SIZE) or not (0 <= y < SIZE):
        print('Такой клетки нет')
        return
    if not grid[x][y]:
        print('В этой клетке нет стрелки')
        return
    if grid[x][y] != direction:
        print('Неверное направление')
        return
    if not path_is_clear(grid, x, y, direction):
        print('Стрелка заблокирована')
        return
    grid[x][y] = None
    print('Стрелка ушла!')

    
def is_empty(grid):
    return not any([cell for row in grid for cell in row])


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

SIZE = int(input())

grid = create_field()
print(is_empty(grid))

grid = generate_field()
print(is_empty(grid))

#draw_field(grid)