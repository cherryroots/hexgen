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

    m1 = Maze(25, 60, num_rows, num_cols, 100, 100, win, 0)
    cell: Hex = m1._cells[3][num_rows // 2]
    neighbors: List[Point] = cell.bounded_neighbors(num_cols, num_rows)
    last = None
    for n in neighbors:
        neighbor: Hex = m1._cells[n.x][n.y]
        if last is None:
            cell.break_between(neighbor)
            neighbor.break_between(cell)
            m1._draw_cells(cell._col, cell._row)
            cell.draw_move(neighbor)
        else:
            last.break_between(neighbor)
            neighbor.break_between(last)
            m1._draw_cells(n.x, n.y)
            last.draw_move(neighbor)
        last = neighbor

    m1._break_entrance_and_exit()

    win.wait_for_close()


main()
