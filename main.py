def create_field():
    grid = []
    for _ in range(SIZE):
        grid.append(input().split())
    return grid

SIZE = int(input())

grid = create_field()
print(grid)