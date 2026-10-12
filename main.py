from game import Game


def get_size() -> int:
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


def main():
    size = get_size()
    game = Game(size)
    game.run()


if __name__ == "__main__":
    main()