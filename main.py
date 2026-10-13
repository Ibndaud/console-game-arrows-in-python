from game import Game


MAX_FIELD_SIZE = 30


def get_size() -> int:
    while True:
        try:
            size = int(input('Введите размер поля: '))
        except ValueError:
            print('Введите целое число')
            continue
        if not 1 <= size <= MAX_FIELD_SIZE:
            print(f'Размер поля должен быть от 1 до {MAX_FIELD_SIZE}')
            continue
        return size


def main():
    size = get_size()
    game = Game(size)
    game.run()


if __name__ == "__main__":
    main()