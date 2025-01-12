from pysudoku.sudoku import Sudoku


class Move:

    def __init__(self, cell: Sudoku.Cell, val: Sudoku.Cell.Option) -> None:
        self._cell = cell
        self._val = val

    def __str__(self) -> str:
        return f"{self.cell}->{self.val}"

    def __repr__(self) -> str:
        return f"Move(cell={self.cell}, val={self.val})"

    @property
    def cell(self) -> Sudoku.Cell:
        return self._cell

    @property
    def val(self) -> Sudoku.Cell.Option:
        return self._val

    def apply(self) -> None:
        self._cell.val = self._val

    def undo(self) -> None:
        self._cell.reset()

    def is_correct(self, sudoku: Sudoku) -> bool:
        return all(
            rel_cell.val != self.val
            for rel_cell in sudoku.related_filled_cells(self.cell)
        )
