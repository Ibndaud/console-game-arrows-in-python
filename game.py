from field import Field
from direction import Direction


class Game:
    def __init__(self, size: int) -> None:
        self.field = Field(size)


    def run(self) -> None:
        while not self.field.is_empty():
            self.game_turn()

        print('Игра окончена!')


    def game_turn(self) -> None:
        while True:
            print(self.field)
            try:
                row, col, direction = input(
                    'Введите номер строки, столбца и направление: '
                    ).split()
                row, col = int(row), int(col)
            except ValueError:
                print('Неверный формат ввода')
                continue
            
            try:
                direction = Direction.from_string(direction)
            except KeyError:
                valid = ', '.join(d.name.lower() for d in Direction)
                print(f'Неизвестное направление. Допустимо: {valid}.')
                continue

            _, message = self.field.make_move(row, col, direction)
            print(message)
            return
