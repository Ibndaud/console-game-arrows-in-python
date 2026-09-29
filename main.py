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


SYMBOLS = {
    'left': '←',
    'right': '→',
    'up': '↑',
    'down': '↓'
}        
SIZE = int(input())

grid = create_field()
draw_field(grid)