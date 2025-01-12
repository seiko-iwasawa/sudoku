from typing import overload, override

from pysudoku.sudoku import Sudoku


class Analyzer(Sudoku):

    class Cell(Sudoku.Cell):

        @override
        def __init__(self, sudoku: Sudoku, cell: Sudoku.Cell) -> None:

            def get_busy_options():
                return {rel_cell.val for rel_cell in sudoku.related_filled_cells(cell)}

            def get_free_options():
                return set(Sudoku.Cell.Option.all()) - get_busy_options()

            super().__init__(cell.row, cell.col, cell.val)
            self._options = {cell.val} if cell.val.filled() else get_free_options()

        @property
        def options(self) -> set[Sudoku.Cell.Option]:
            return self._options

    class Counter:

        type Group = list[dict[Sudoku.Cell.Option, int]]

        def __init__(self) -> None:
            init_group = lambda: [
                dict.fromkeys(Sudoku.Cell.Option.all(), 0) for n in range(Sudoku.N)
            ]
            self._rows = init_group()
            self._cols = init_group()
            self._blocks = init_group()

        @property
        def rows(self) -> Group:
            return self._rows

        @property
        def cols(self) -> Group:
            return self._cols

        @property
        def blocks(self) -> Group:
            return self._blocks

        def add(self, cell: Sudoku.Cell, option: Sudoku.Cell.Option) -> None:
            self.rows[cell.row][option] += 1
            self.cols[cell.col][option] += 1
            self.blocks[cell.block][option] += 1

        def has_zero(self) -> bool:
            for group in [self.rows, self.cols, self.blocks]:
                for cnt in group:
                    if not all(cnt.values()):
                        return True
            return False

    def _build_grid(self, sudoku: Sudoku) -> None:
        self._grid = [
            [Analyzer.Cell(sudoku, sudoku[i][j]) for j in range(Sudoku.N)]
            for i in range(Sudoku.N)
        ]

    def _build_counter(self) -> None:
        self._counter = Analyzer.Counter()
        for cell in self.cells:
            for option in self[cell]:
                self._counter.add(cell, option)

    @override
    def __init__(self, sudoku: Sudoku) -> None:
        self._build_grid(sudoku)
        self._build_counter()

    @overload
    def __getitem__(self, ind: int) -> Sudoku.Row: ...

    @overload
    def __getitem__(self, ind: Sudoku.Cell) -> set[Sudoku.Cell.Option]: ...

    @override
    def __getitem__(self, ind: int | Sudoku.Cell):
        if isinstance(ind, int):
            return super().__getitem__(ind)
        else:
            return self._grid[ind.row][ind.col].options

    def _has_unfillable_cell(self) -> bool:
        return any(not self[cell] for cell in self.empty_cells)

    def check(self) -> bool:
        return not self._has_unfillable_cell() and not self._counter.has_zero()

    def row_occ(self, row: int, option: Sudoku.Cell.Option) -> int:
        return self._counter.rows[row][option]

    def col_occ(self, col: int, option: Sudoku.Cell.Option) -> int:
        return self._counter.cols[col][option]

    def block_occ(self, block: int, option: Sudoku.Cell.Option) -> int:
        return self._counter.blocks[block][option]
