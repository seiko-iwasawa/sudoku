import unittest

from pysudoku.solverHuman import SolverHuman
from pysudoku.solverStupid import SolverStupid
from pysudoku.sudoku import Sudoku


class TestCommon(unittest.TestCase):

    def setUp(self):
        self.easy_sudoku = Sudoku.from_grid(
            [
                [0, 6, 4, 2, 9, 7, 3, 0, 0],
                [2, 7, 9, 5, 3, 0, 0, 0, 0],
                [0, 8, 0, 0, 0, 0, 0, 0, 7],
                [5, 1, 0, 0, 6, 2, 8, 0, 0],
                [9, 0, 0, 0, 0, 0, 0, 6, 0],
                [6, 0, 7, 8, 4, 0, 0, 0, 0],
                [0, 0, 0, 1, 7, 4, 9, 2, 5],
                [4, 9, 0, 0, 0, 0, 0, 8, 6],
                [7, 5, 2, 6, 8, 9, 4, 0, 3],
            ]
        )
        self.hard_sudoku = Sudoku.from_grid(
            [
                [0, 0, 0, 0, 5, 9, 7, 8, 0],
                [6, 0, 0, 0, 0, 0, 2, 9, 0],
                [0, 9, 0, 0, 7, 6, 0, 0, 0],
                [2, 0, 9, 3, 0, 0, 4, 0, 7],
                [7, 0, 8, 5, 9, 4, 0, 0, 0],
                [0, 0, 0, 7, 0, 0, 8, 0, 9],
                [0, 0, 5, 0, 0, 0, 0, 7, 0],
                [0, 4, 0, 6, 0, 0, 0, 0, 0],
                [0, 0, 0, 9, 0, 0, 0, 0, 0],
            ]
        )

    def test_stupid_solver(self):
        SolverStupid(self.easy_sudoku).run()
        self.assertTrue(self.easy_sudoku.filled() and self.easy_sudoku.is_correct())

    def test_human_solver(self):
        SolverHuman(self.hard_sudoku, explain=True).run()
        self.assertTrue(self.hard_sudoku.filled() and self.hard_sudoku.is_correct())

    def test_no_solution(self):
        self.hard_sudoku[8][8].val = Sudoku.Cell.Option(1)
        SolverHuman(self.hard_sudoku).run()
        self.assertTrue(not self.hard_sudoku.filled() and self.hard_sudoku.is_correct())
