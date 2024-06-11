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


class Hex:
    def __init__(self, col: int, row: int, win: Window = None, walls: int = 6) -> None:
        self.walls = [True] * walls
        self._col = col
        self._row = row
        self.q, self.r = oddr_to_axial(self._col, self._row)
        self.s = -self.q - self.r
        self._cx, self._cy = 0, 0
        self.visited = False
        self.__win = win

    def __repr__(self) -> str:
        return f"(Hex(({self._col}, {self._row}), {self.walls}, {self.visited})"

    def __eq__(self, other: "Hex"):
        return self.q == other.q and self.r == other.r and self.s == other.s

    def __nq__(self, other: "Hex"):
        return not (self == other)

    def __add__(self, other: "Hex") -> "Hex":
        axial = axial_to_oddr(self.q + other.q, self.r + other.r)
        return Hex(*axial)

    def __sub__(self, other: "Hex") -> "Hex":
        axial = axial_to_oddr(self.q + other.q, self.r + other.r)
        return Hex(*axial)

    def corners(self, width: int, height: int) -> List[Tuple[int, int]]:
        walls = len(self.walls)
        offsetAngle = pi / walls
        corners = []
        for i in range(walls):
            x = self._cx + (width / 2) * cos(offsetAngle - i * 2 * pi / walls)
            y = self._cy + (height / 2) * sin(offsetAngle - i * 2 * pi / walls)
            corners.append((x, y))
        return corners

    def direction(self, direction: int):
        return hex_directions[(6 + (direction % 6)) % 6]

    def neighbor(self, direction: int):
        return self + self.direction(direction)

    def neignbors(self) -> List[Point]:
        neighbors = []
        for i in range(6):
            neighbor: Hex = self.neighbor(i)
            coords = Point(*axial_to_oddr(neighbor.q, neighbor.r))
            neighbors.append(coords)

        return neighbors

    def bounded_neighbors(self, cols: int, rows: int) -> List[Point]:
        discard_filter = filter(
            lambda p: p.x >= 0 and p.x < cols and p.y >= 0 and p.y < rows,
            self.neignbors(),
        )
        return list(discard_filter)

    def draw(self, cx: float, cy: float, width: int, height: int) -> None:
        self._cx, self._cy = cx, cy

        corners = self.corners(width, height)

        corners = [Point(*corner) for corner in corners]
        lines = [Line(p1, p2) for p1, p2 in zip(corners, corners[1:] + [corners[0]])]

        for wall, line in zip(self.walls, lines):
            self.__win.draw(line, "black" if wall else "white", 2 if wall else 4)

        """
        text = Text(
            f"c{self._col}, r{self._row}\n\nq{self.q}, r{self.r}\n  s{self.s}",
            Point(self._cx, self._cy),
        )
        self.__win.draw_text(text)
        """

    def draw_move(self, other: "Hex", undo: bool = False):
        origin = Point(self._cx, self._cy)
        destination = Point(other._cx, other._cy)
        line = Line(origin, destination)
        self.__win.draw(line, "gray" if undo else "red")

    def break_wall(self, direction: int):
        self.walls[direction] = False

    def wall_towards(self, direction: int):
        return self.walls[direction]

    def break_between(self, other: "Hex"):
        delta_q = other.q - self.q
        delta_r = other.r - self.r

        if delta_q == 1 and delta_r == 0:  # E
            self.break_wall(0)
        if delta_q == 1 and delta_r == -1:  # NE
            self.break_wall(1)
        if delta_q == 0 and delta_r == -1:  # NW
            self.break_wall(2)
        if delta_q == -1 and delta_r == 0:  # W
            self.break_wall(3)
        if delta_q == -1 and delta_r == 1:  # SW
            self.break_wall(4)
        if delta_q == 0 and delta_r == 1:  # SE
            self.break_wall(5)

    def wall_between(self, other: "Hex"):
        delta_q = other.q - self.q
        delta_r = other.r - self.r

        if delta_q == 1 and delta_r == 0:  # E
            return self.wall_towards(0)
        if delta_q == 1 and delta_r == -1:  # NE
            return self.wall_towards(1)
        if delta_q == 0 and delta_r == -1:  # NW
            return self.wall_towards(2)
        if delta_q == -1 and delta_r == 0:  # W
            return self.wall_towards(3)
        if delta_q == -1 and delta_r == 1:  # SW
            return self.wall_towards(4)
        if delta_q == 0 and delta_r == 1:  # SE
            return self.wall_towards(5)


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
