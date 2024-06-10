from math import sqrt
from time import sleep
from hex import Hex
from graphics import Window
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
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        self._cells = []  # list of columns of rows
        self._create_cells()

    def _create_cells(self):
        for i in range(self._num_cols):
            column = []
            for j in range(self._num_rows):
                column.append(Hex(i, j, self._win))
            self._cells.append(column)

        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._draw_cells(i, j)

    def _draw_cells(self, i, j):
        if self._win is None:
            return

        horiz = sqrt(3) * self._cell_size_y / 2
        vert = 3 / 2 * self._cell_size_x / 2
        horiz_offset = horiz / 2 if j % 2 != False else 0

        top_left_x = self._y1 + i * horiz
        top_left_y = self._y1 + j * vert
        bottom_right_x = top_left_x + self._cell_size_x
        bottom_right_y = top_left_y + self._cell_size_y

        cx = ((top_left_x + bottom_right_x) / 2) + horiz_offset
        cy = (top_left_y + bottom_right_y) / 2

        hex: Hex = self._cells[i][j]
        hex.draw(cx, cy, self._cell_size_x, self._cell_size_y)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        sleep(0.01)
