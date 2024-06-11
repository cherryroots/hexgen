import unittest

from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells1(self):
        num_cols = 12
        num_rows = 10

        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_create_cells2(self):
        num_cols = 500
        num_rows = 500

        m1 = Maze(0, 0, num_rows, num_cols, 1, 1)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_reset_cells_visited(self):
        num_cols = 15
        num_rows = 15
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._break_walls_r(0, 0)
        m1._reset_visited()
        for col in m1._cells:
            for cell in col:
                self.assertEqual(cell.visited, False)


if __name__ == "__main__":
    unittest.main()
