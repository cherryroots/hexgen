from math import sqrt
import random
from time import sleep

from hex import Hex
from graphics import Window, Point
from typing import List


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window = None,
        start: Point = None,
        end: Point = None,
        seed=None,
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        self._start = Point(0, 0) if start is None else start
        self._end = (
            Point(self._num_cols - 1, self._num_rows - 1) if end is None else end
        )

        if seed:
            random.seed(seed)

        self._cells: List[List[Hex]] = []  # list of columns of rows
        self._create_cells()

    def _create_cells(self) -> None:
        for i in range(self._num_cols):
            column = []
            for j in range(self._num_rows):
                column.append(Hex(i, j, self._win))
            self._cells.append(column)

        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._draw_cells(i, j)

    def _draw_cells(self, i: int, j: int) -> None:
        if self._win is None:
            return

        horiz = sqrt(3) * self._cell_size_y / 2
        vert = 3 / 2 * self._cell_size_x / 2
        horiz_offset = horiz / 2 if j % 2 != False else 0

        top_left_x = self._x1 + i * horiz
        top_left_y = self._y1 + j * vert
        bottom_right_x = top_left_x + self._cell_size_x
        bottom_right_y = top_left_y + self._cell_size_y

        cx = ((top_left_x + bottom_right_x) / 2) + horiz_offset
        cy = (top_left_y + bottom_right_y) / 2

        hex = self._cells[i][j]
        hex.draw(cx, cy, self._cell_size_x, self._cell_size_y)
        self._animate()

    def _animate(self) -> None:
        if self._win is None:
            return
        self._win.redraw()
        sleep(0.01)

    def _reset_visited(self) -> None:
        for col in self._cells:
            for hex in col:
                hex.visited = False

    def _break_entrance_and_exit(self) -> None:
        start = self._cells[self._start.x][self._start.y]
        end = self._cells[self._end.x][self._end.y]
        start.break_wall(2)
        self._draw_cells(start._col, start._row)
        end.break_wall(5)
        self._draw_cells(end._col, end._row)

    def _break_walls_r(self, i: int, j: int) -> None:
        current = self._cells[i][j]
        current.visited = True
        while True:
            to_visit = []
            neighbors = current.bounded_neighbors(self._num_cols, self._num_rows)
            for point in neighbors:
                neighbor = self._cells[point.x][point.y]
                if not neighbor.visited:
                    to_visit.append(point)

            if len(to_visit) == 0:
                self._draw_cells(i, j)
                return

            direction = random.randrange(len(to_visit))
            point = to_visit[direction]
            next = self._cells[point.x][point.y]

            current.break_between(next)
            next.break_between(current)
            self._break_walls_r(point.x, point.y)

    def _solve_r(self, i: int, j: int):
        self._animate()

        current = self._cells[i][j]
        current.visited = True

        if i == self._end.x and j == self._end.y:
            return True

        neighbors = current.bounded_neighbors(self._num_cols, self._num_rows)

        for point in neighbors:
            neighbor = self._cells[point.x][point.y]
            if neighbor.visited:
                continue
            if current.wall_between(neighbor) or neighbor.wall_between(current):
                continue
            current.draw_move(neighbor)
            if self._solve_r(neighbor._col, neighbor._row):
                return True
            current.draw_move(neighbor, undo=True)

        return False

    def solve(self):
        return self._solve_r(*self._start.xy())
