from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import override

from pysudoku.analyzer import Analyzer
from pysudoku.move import Move
from pysudoku.sudoku import Sudoku


class Solver(ABC):
    def __init__(self, sudoku: Sudoku) -> None:
        self._sudoku = sudoku

    @abstractmethod
    def predict_move(self) -> Generator[Move]: ...

    def try_move(self, move: Move) -> bool:
        move.apply()
        if not (solved := self.rec_solve()):
            move.undo()
        return solved

    def rec_solve(self) -> bool:
        return (self._sudoku.filled() and self._sudoku.is_correct()) or any(
            self.try_move(move) for move in self.predict_move()
        )

    def run(self) -> bool:
        return self._sudoku.is_correct() and self.rec_solve()


class SolverStupid(Solver):

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


class InfoMove(Move):

    @override
    def __init__(
        self, cell: Sudoku.Cell, val: Sudoku.Cell.Option, info: str | None = None
    ) -> None:
        super().__init__(cell, val)
        self._info = info or "unknown reason"

    @override
    def __str__(self) -> str:
        return f"{self.cell}->{self.val} ({self.info})"

    @override
    def __repr__(self) -> str:
        return f"Move(cell={self.cell}, val={self.val}, info='{self.info}'))"

    @property
    def info(self) -> str:
        return self._info


class SolverHuman(Solver):

    def __init__(self, sudoku: Sudoku, explain: bool = False) -> None:
        super().__init__(sudoku)
        self._explain = explain
        self._complexity = 0
        self._depth = 0

    def _move(
        self, cell: Sudoku.Cell, val: Sudoku.Cell.Option, info: str, complexity: int
    ) -> InfoMove:
        move = InfoMove(cell, val, info)
        self._complexity += complexity
        if self._explain:
            print("." * self._depth + str(move))
        return move

    def _easy_move(self, analyzer: Analyzer) -> InfoMove | None:
        for cell in self._sudoku.empty_cells:
            if len(analyzer[cell]) == 1:
                val = next(iter(analyzer[cell]))
                return self._move(cell, val, "other options are blocked", 1)
        return None

    def _get_unique_group(
        self, analyzer: Analyzer, cell: Sudoku.Cell, val: Sudoku.Cell.Option
    ) -> str | None:
        if analyzer.row_occ(cell.row, val) == 1:
            return "row"
        elif analyzer.col_occ(cell.col, val) == 1:
            return "col"
        elif analyzer.block_occ(cell.block, val) == 1:
            return "block"
        return None

    def _medium_move(self, analyzer: Analyzer) -> InfoMove | None:
        for cell in self._sudoku.empty_cells:
            for val in analyzer[cell]:
                if group := self._get_unique_group(analyzer, cell, val):
                    return self._move(
                        cell, val, f"according {group} has only one occurrence", 5
                    )
        return None

    def _brute_force(self, analyzer: Analyzer) -> Generator[InfoMove]:
        cell = min(self._sudoku.empty_cells, key=lambda cell: len(analyzer[cell]))
        self._complexity += 25 * len(analyzer[cell])
        self._depth += 1
        for val in analyzer[cell]:
            yield self._move(cell, val, "brute force", 0)
        self._depth -= 1

    def predict_move(self) -> Generator[InfoMove]:
        options = Analyzer(self._sudoku)
        if not options.check():
            ...
        elif move := self._easy_move(options):
            yield move
        elif move := self._medium_move(options):
            yield move
        else:
            yield from self._brute_force(options)
