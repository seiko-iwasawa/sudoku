from collections.abc import Generator
from typing import override

from pysudoku.solverABC import Move, SolverABC, Sudoku


class SolverStupid(SolverABC):

    @override
    def __init__(self, sudoku: Sudoku) -> None:
        super().__init__(sudoku)
        self._empty_cells = list(self._sudoku.empty_cells)

    @override
    def predict_move(self) -> Generator[Move]:

        def get_free_options(cell: Sudoku.Cell):
            return set(Sudoku.Cell.Option.all()).difference(
                cell.val for cell in self._sudoku.related_filled_cells(cell)
            )

        for val in get_free_options(empty_cell := self._empty_cells.pop()):
            yield Move(empty_cell, val)
        self._empty_cells.append(empty_cell)
