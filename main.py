from graphics import (
    Window,
    Point,
    Line,
)
from maze import Maze
from hex import Hex
from typing import List


def main():
    win = Window(800, 600)

    num_cols = (win.width) // 100
    num_rows = (win.height) // 100

    m1 = Maze(25, 60, num_rows, num_cols, 100, 100, win, 10)

    m1._break_walls_r(0, 0)
    m1._reset_visited()
    m1._break_entrance_and_exit()
    m1.solve()

    win.wait_for_close()


main()
