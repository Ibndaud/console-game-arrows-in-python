from enum import Enum
from typing import Self

class Direction(Enum):
    LEFT = (0, -1, '←')
    RIGHT = (0, 1, '→')
    UP = (-1, 0, '↑')
    DOWN = (1, 0, '↓')

    def __init__(self, dr: int, dc: int, symbol: str) -> None:
        self.dr = dr
        self.dc = dc
        self.symbol = symbol
    
    @classmethod
    def from_string(cls, value: str) -> Self:
        return cls[value.strip().upper()]

    def apply(self, cell: tuple[int, int]) -> tuple[int, int]:
        row, col = cell
        return row + self.dr, col + self.dc
