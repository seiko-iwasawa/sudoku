from collections.abc import Generator
from copy import deepcopy
from typing import Literal, override

from pysudoku.analyzer import Analyzer
from pysudoku.solverABC import Move, SolverABC, Sudoku


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


class SolverHuman(SolverABC):

    def __init__(self, sudoku: Sudoku, explain: bool = False) -> None:
        super().__init__(sudoku)
        self._complexity: int = 0
        self._explain = explain

    def _easy_move(self, analyzer: Analyzer) -> InfoMove | None:
        for cell in self._sudoku.empty_cells:
            if len(analyzer[cell]) == 1:
                for val in analyzer[cell]:
                    ...
                return InfoMove(cell, val, "other options are blocked")

    def _medium_move(self, analyzer: Analyzer) -> InfoMove | None:
        for cell in self._sudoku.empty_cells:
            for val in analyzer[cell]:
                group = None
                if analyzer.row_occ(cell.row, val) == 1:
                    group = "row"
                elif analyzer.col_occ(cell.col, val) == 1:
                    group = "col"
                elif analyzer.block_occ(cell.block, val) == 1:
                    group = "block"
                if group:
                    return InfoMove(
                        cell, val, f"according {group} has only one occurrence"
                    )

    def _brute_force(self, analyzer: Analyzer) -> Generator[InfoMove]:
        cell = min(self._sudoku.empty_cells, key=lambda cell: len(analyzer[cell]))
        self._complexity += 25 ** len(analyzer[cell])
        for val in analyzer[cell]:
            self.record("branch-in", InfoMove(cell, val, "brute force"))
            yield InfoMove(cell, val)
            self.record("branch-out", InfoMove(cell, val, "no solution"))

    def record(
        self,
        mode: Literal[
            "easy", "medium", "brute force", "branch-in", "branch-out"
        ],
        move: InfoMove,
    ) -> None:
        if mode == "easy":
            self._complexity += 1
        elif mode == "medium":
            self._complexity += 5
        if self._explain:
            print(move)

    def predict_move(self) -> Generator[InfoMove]:
        options = Analyzer(self._sudoku)
        if not options.check():
            ...
        elif move := self._easy_move(options):
            self.record("easy", move)
            yield move
        elif move := self._medium_move(options):
            self.record("medium", move)
            yield move
        else:
            yield from self._brute_force(options)
