from math import cos, pi, sin
from typing import (
    List,
    Tuple,
)
from graphics import (
    Window,
    Point,
    Line,
    Text,
)


class OffsetCoord:
    def __init__(self, col: int, row: int):
        self.col, self.row = col, row

    def coords(self) -> Tuple[int, int]:
        return self.col, self.row


class Hex:
    def __init__(self, col: int, row: int, win: Window = None, walls: int = 6) -> None:
        self.walls = [True] * walls
        self._col = col
        self._row = row
        self.q, self.r = oddr_to_axial(self._col, self._row)
        self.s = -self.q - self.r
        if self.q + self.r + self.s != 0:
            raise Exception("invalid hex")
        self._cx, self._cy = 0, 0
        self.__win = win

    def __eq__(self, other):
        return self.q == other.q and self.r == other.r and self.s == other.s

    def __nq__(self, other):
        return not (self == other)

    def __add__(self, other):
        return Hex(self.q + other.q, self.r + other.r, self.s + other.s)

    def __sub__(self, other):
        return Hex(self.q - other.q, self.r - other.r, self.s - other.s)

    def __mul__(self, other: int):
        return Hex(self.q * other, self.r * other, self.s * other)

    def corners(self, width: int, height: int) -> List[Tuple[int, int]]:
        walls = len(self.walls)
        offsetAngle = pi / walls
        corners = []
        for i in range(walls):
            x = self._cx + (width / 2) * cos(offsetAngle - i * 2 * pi / walls)
            y = self._cy + (height / 2) * sin(offsetAngle - i * 2 * pi / walls)
            corners.append((x, y))
        return corners

    def hex_direction(self, direction: int):
        return hex_directions[(6 + (direction % 6)) % 6]

    def hex_length(self, other):
        return int((abs(other.q) + abs(other.r) + abs(other.s)) / 2)

    def hex_distance(self, other):
        return self.hex_length(self.hex_subtract(self, other))

    def draw(self, cx: float, cy: float, width: int, height: int) -> None:
        self._cx, self._cy = cx, cy
        text = Text(f"q{self.q}, r{self.r}\n  s{self.s}", Point(self._cx, self._cy))

        corners = self.corners(width, height)

        corners = [Point(*corner) for corner in corners]
        lines = [Line(p1, p2) for p1, p2 in zip(corners, corners[1:] + [corners[0]])]

        for wall, line in zip(self.walls, lines):
            self.__win.draw(line, "black" if wall else "white")

        self.__win.draw_text(text)

    def draw_move(self, to_cell, undo: bool = False):
        origin = Point(self._cx, self._cy)
        destination = Point(to_cell._cx, to_cell._cy)
        line = Line(origin, destination)
        self.__win.draw(line, "gray" if undo else "red")

    def break_between(self, to_cell):
        pass


def axial_to_oddr(q: int, r: int):
    col = q + int((r - (r & 1)) / 2)
    row = r
    return col, row


def oddr_to_axial(col: int, row: int):
    q = col - int((row - (row & 1)) / 2)
    r = row
    return q, r


hex_directions = [
    Hex(*axial_to_oddr(1, 0)),  # 0 E
    Hex(*axial_to_oddr(1, -1)),  # 1 NE
    Hex(*axial_to_oddr(0, -1)),  # 2 NW
    Hex(*axial_to_oddr(-1, 0)),  # 3 W
    Hex(*axial_to_oddr(-1, 1)),  # 4 SW
    Hex(*axial_to_oddr(0, 1)),  # 5 SE
]
