def create_field():
    grid = []
    for _ in range(SIZE):
        grid.append(input().split())
    return grid


def draw_field(grid):
    for i in range(SIZE + 1):
        if not i:
            print('\t' + '\t'.join(map(str, range(1, SIZE + 1))))
            continue
        print(str(i) + '\t' + '\t'.join(grid[i - 1]))
        
        
SIZE = int(input())

grid = create_field()
draw_field(grid)