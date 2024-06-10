from graphics import (
    Window,
    Point,
    Line,
)
from maze import Maze


def main():
    win = Window(800, 600)

    # num_cols = (win.width) // 40
    # num_rows = (win.height) // 35

    # m1 = Maze(40, 40, num_rows, num_cols, 40, 40, win)

    num_cols = (win.width) // 100
    num_rows = (win.height) // 100

    m1 = Maze(40, 40, num_rows, num_cols, 100, 100, win)

    win.wait_for_close()


main()
