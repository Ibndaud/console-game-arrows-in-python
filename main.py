def create_field():
    grid = []
    for _ in range(SIZE):
        grid.append([i if i != '.' else None for i in input().split()])
    return grid


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

row, col, direction = input().split()
row, col = int(row), int(col)

print(f"Стрелка {('заблокирована', 'ушла!')[path_is_clear(grid, row, col, direction)]}")