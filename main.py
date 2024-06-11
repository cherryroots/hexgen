from time import sleep
from graphics import (
    Window,
    Point,
)
from maze import Maze


def main():
    win = Window(800, 600)

    num_cols = (win.width) // 45
    num_rows = (win.height) // 40

    for i in range(0, num_cols, num_cols // 2):
        win.clear()
        start = Point(0 + i, 0)
        end = Point(num_cols - 1 - i, num_rows - 1)
        m = Maze(20, 15, num_rows, num_cols, 50, 50, win, start, end)

        m._break_entrance_and_exit()
        m._break_walls_r(*start.xy())
        m._reset_visited()
        m.solve()
        sleep(2)

    win.wait_for_close()


main()
