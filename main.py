from graphics import (
    Window,
    Point,
    Line,
)
from maze import Maze
from hex import Hex


def main():
    win = Window(800, 600)

    # num_cols = (win.width) // 40
    # num_rows = (win.height) // 35

    # m1 = Maze(40, 40, num_rows, num_cols, 40, 40, win)

    num_cols = (win.width) // 100
    num_rows = (win.height) // 100

    m1 = Maze(40, 40, num_rows, num_cols, 100, 100, win)
    cell: Hex = m1._cells[1][1]
    neighbors = cell.hex_neignbors()
    last = None
    for n in neighbors:
        neighbor: Hex = m1._cells[n[0]][n[1]]
        if last is None:
            cell.break_between(neighbor)
            neighbor.break_between(cell)
            m1._draw_cells(1, 1)
            cell.draw_move(neighbor)
        else:
            last.break_between(neighbor)
            neighbor.break_between(last)
            m1._draw_cells(n[0], n[1])
            last.draw_move(neighbor)
        last = neighbor

    print(m1._cells[1][1].walls)
    print(m1._cells[2][1].walls)
    print(m1._cells[2][0].walls)
    print(m1._cells[1][0].walls)
    print(m1._cells[0][1].walls)
    print(m1._cells[1][2].walls)
    print(m1._cells[2][2].walls)

    win.wait_for_close()


main()
