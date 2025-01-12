import io
import sys
import unittest

from pysudoku.sudoku import Sudoku


class TestOption(unittest.TestCase):

    def setUp(self):
        self.val0 = Sudoku.Cell.Option(0)
        self.val5 = Sudoku.Cell.Option(5)

    def test_init(self):
        self.assertRaises(ValueError, Sudoku.Cell.Option, 10)
        Sudoku.Cell.Option(9)

    def test_from_str(self):
        Sudoku.Cell.Option.from_str(".")
        Sudoku.Cell.Option.from_str("0")
        Sudoku.Cell.Option.from_str("9")
        self.assertRaises(ValueError, Sudoku.Cell.Option.from_str, "10")
        self.assertRaises(ValueError, Sudoku.Cell.Option.from_str, "abc")
        self.assertRaises(ValueError, Sudoku.Cell.Option.from_str, "-1")

    def test_int(self):
        self.assertEqual(int(self.val5), 5)

    def test_str(self):
        self.assertEqual(str(self.val0), ".")
        self.assertEqual(str(self.val5), "5")

    def test_repr(self):
        self.assertEqual(repr(self.val5), "Option(_val=5)")

    def test_bool(self):
        self.assertEqual(bool(self.val0), False)
        self.assertEqual(bool(self.val5), True)

    def test_eq(self):
        self.assertEqual(self.val5, Sudoku.Cell.Option(5))
        self.assertNotEqual(self.val5, self.val0)

    def test_hash(self):
        self.assertEqual(hash(self.val5), hash(5))

    def test_empty(self):
        self.assertTrue(self.val0.empty())
        self.assertFalse(self.val5.empty())

    def test_filled(self):
        self.assertFalse(self.val0.filled())
        self.assertTrue(self.val5.filled())

    def test_all(self):
        self.assertEqual(
            list(Sudoku.Cell.Option.all()), list(map(Sudoku.Cell.Option, range(1, 10)))
        )


class TestCell(unittest.TestCase):

    def setUp(self):
        self.cell = Sudoku.Cell(3, 8, Sudoku.Cell.Option(7))

    def test_row(self):
        self.assertEqual(self.cell.row, 3)

    def test_col(self):
        self.assertEqual(self.cell.col, 8)

    def test_block(self):
        self.assertEqual(self.cell.block, 5)

    def test_val(self):

        def try_set_value():
            self.cell.val = Sudoku.Cell.Option(1)

        self.assertEqual(self.cell.val, Sudoku.Cell.Option(7))
        self.assertRaises(ValueError, try_set_value)
        self.cell.reset()
        self.assertEqual(self.cell.val, Sudoku.Cell.Option(0))
        self.cell.val = Sudoku.Cell.Option(5)
        self.assertEqual(self.cell.val, Sudoku.Cell.Option(5))

    def test_empty(self):
        self.assertFalse(self.cell.empty())

    def test_filled(self):
        self.assertTrue(self.cell.filled())

    def test_str(self):
        self.assertEqual(str(self.cell), "[4, 9]-7")

    def test_repr(self):
        self.assertEqual(repr(self.cell), "Cell(row=3, col=8, val=7)")


class TestSudoku(unittest.TestCase):

    def setUp(self):
        self.empty_sudoku = Sudoku()
        self.sudoku = Sudoku.from_grid(
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

    def test_from_iter(self):
        self.assertEqual(repr(Sudoku.from_iter(iter([]))), repr(self.empty_sudoku))

    def test_from_grid(self):
        self.assertRaises(
            ValueError, Sudoku.from_grid, [[1, 2], [3, 4], [], [], [], [], [], [], []]
        )

    def test_from_str(self):
        self.assertEqual(
            repr(
                Sudoku.from_str(
                    """\
╔═══════╦═══════╦═══════╗
║ . . . ║ . 5 9 ║ 7 8 . ║
║ 6 . . ║ . . . ║ 2 9 . ║
║ . 9 . ║ . 7 6 ║ . . . ║
╠═══════╬═══════╬═══════╣
║ 2 . 9 ║ 3 . . ║ 4 . 7 ║
║ 7 . 8 ║ 5 9 4 ║ . . . ║
║ . . . ║ 7 . . ║ 8 . 9 ║
╠═══════╬═══════╬═══════╣
║ . . 5 ║ . . . ║ . 7 . ║
║ . 4 . ║ 6 . . ║ . . . ║
║ . . . ║ 9 . . ║ . . . ║
╚═══════╩═══════╩═══════╝"""
                )
            ),
            repr(self.sudoku),
        )

    def test_from_input(self):
        sys.stdin = io.StringIO(
            """\
....5978
6.....29.
.9..76
2.93..4.7
7.8594..
...7..8.9
..5....7
.4.6..
...9
"""
        )
        self.assertEqual(repr(Sudoku.from_input()), repr(self.sudoku))

    def test_is_related(self):
        self.assertFalse(Sudoku.is_related(Sudoku.Cell(2, 5), Sudoku.Cell(8, 1)))
        self.assertTrue(Sudoku.is_related(Sudoku.Cell(3, 3), Sudoku.Cell(4, 5)))
        self.assertTrue(Sudoku.is_related(Sudoku.Cell(1, 6), Sudoku.Cell(7, 6)))

    def test_getitem(self):
        self.assertEqual(repr(self.empty_sudoku[3][2]), "Cell(row=3, col=2, val=0)")
        self.assertEqual(repr(self.sudoku[3][2]), "Cell(row=3, col=2, val=9)")

    def test_str(self):
        self.assertEqual(
            str(self.sudoku),
            """\
╔═══════╦═══════╦═══════╗
║ . . . ║ . 5 9 ║ 7 8 . ║
║ 6 . . ║ . . . ║ 2 9 . ║
║ . 9 . ║ . 7 6 ║ . . . ║
╠═══════╬═══════╬═══════╣
║ 2 . 9 ║ 3 . . ║ 4 . 7 ║
║ 7 . 8 ║ 5 9 4 ║ . . . ║
║ . . . ║ 7 . . ║ 8 . 9 ║
╠═══════╬═══════╬═══════╣
║ . . 5 ║ . . . ║ . 7 . ║
║ . 4 . ║ 6 . . ║ . . . ║
║ . . . ║ 9 . . ║ . . . ║
╚═══════╩═══════╩═══════╝""",
        )

    def test_repr(self):
        self.assertEqual(
            repr(self.sudoku),
            "Sudoku(_grid=[[0, 0, 0, 0, 5, 9, 7, 8, 0], [6, 0, 0, 0, 0, 0, 2, 9, 0], "
            "[0, 9, 0, 0, 7, 6, 0, 0, 0], [2, 0, 9, 3, 0, 0, 4, 0, 7], [7, 0, 8, 5, 9, "
            "4, 0, 0, 0], [0, 0, 0, 7, 0, 0, 8, 0, 9], [0, 0, 5, 0, 0, 0, 0, 7, 0], "
            "[0, 4, 0, 6, 0, 0, 0, 0, 0], [0, 0, 0, 9, 0, 0, 0, 0, 0]])",
        )

    def test_cell(self):
        self.assertEqual(
            repr(self.empty_sudoku.cell(3, 2)), "Cell(row=3, col=2, val=0)"
        )
        self.assertEqual(repr(self.sudoku.cell(3, 2)), "Cell(row=3, col=2, val=9)")

    def test_cells(self):
        self.assertEqual(len(list(self.sudoku.cells)), 81)

    def test_empty_cells(self):
        self.assertEqual(len(list(self.empty_sudoku.empty_cells)), 81)
        self.assertEqual(len(list(self.sudoku.empty_cells)), 53)

    def test_filled_cells(self):
        self.assertEqual(len(list(self.empty_sudoku.filled_cells)), 0)
        self.assertEqual(len(list(self.sudoku.filled_cells)), 28)

    def test_row(self):
        self.assertEqual(
            self.sudoku.row(5),
            [self.sudoku.cell(5, col) for col in range(9)],
        )

    def test_rows(self):
        self.assertEqual(
            list(self.sudoku.rows),
            [self.sudoku.row(n) for n in range(9)],
        )

    def test_col(self):
        self.assertEqual(
            self.sudoku.col(5), [self.sudoku.cell(row, 5) for row in range(9)]
        )

    def test_cols(self):
        self.assertEqual(list(self.sudoku.cols), [self.sudoku.col(n) for n in range(9)])

    def test_block(self):
        self.assertEqual(
            self.sudoku.block(3),
            [self.sudoku.cell(3 + i, j) for i in range(3) for j in range(3)],
        )

    def test_blocks(self):
        self.assertEqual(
            list(self.sudoku.blocks), [self.sudoku.block(n) for n in range(9)]
        )

    def test_related_cells(self):
        self.assertEqual(len(list(self.sudoku.related_cells(self.sudoku[7][3]))), 20)

    def test_related_empty_cells(self):
        self.assertEqual(
            len(list(self.sudoku.related_empty_cells(self.sudoku[7][3]))), 15
        )

    def test_related_filled_cells(self):
        self.assertEqual(
            len(list(self.sudoku.related_filled_cells(self.sudoku[7][3]))), 5
        )

    def test_conflict(self):
        self.assertIs(self.empty_sudoku.conflict(), None)
        self.assertIs(self.sudoku.conflict(), None)
        self.sudoku[7][4].val = Sudoku.Cell.Option(5)
        self.assertEqual(self.sudoku.conflict(), (self.sudoku[0][4], self.sudoku[7][4]))

    def test_is_correct(self):
        self.assertTrue(self.sudoku.is_correct())
        self.sudoku[7][4].val = Sudoku.Cell.Option(5)
        self.assertFalse(self.sudoku.is_correct())

    def test_empty(self):
        self.assertTrue(self.empty_sudoku.empty())
        self.assertFalse(self.sudoku.empty())

    def test_filled(self):
        self.assertFalse(self.empty_sudoku.filled())
        self.assertFalse(self.sudoku.filled())

    def test_clear(self):
        self.assertFalse(self.sudoku.empty())
        self.sudoku.clear()
        self.assertTrue(self.sudoku.empty())
