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


class Tree:

    def __init__(self, analyzer: Analyzer, depth: int, move: InfoMove) -> None:
        self._analyzer = deepcopy(analyzer)
        self._depth = depth
        self._move = move
        self._branches: list[Tree] = []
        self._no_solution = False
        self._build()

    @property
    def no_solution(self) -> bool:
        return self._no_solution

    def _brute_force_order(self) -> list[Sudoku.Cell]:
        first: list[Sudoku.Cell] = []
        later: list[Sudoku.Cell] = []
        for cell in self._analyzer.empty_cells:
            (first if Sudoku.is_related(cell, self._move.cell) else later).append(cell)
        return first + later

    def _build_branch(self, move: InfoMove) -> bool:
        branch = Tree(self._analyzer, self._depth - 1, move)
        self._branches.append(branch)
        return branch.no_solution

    def _brute_force_cell(self, cell: Sudoku.Cell) -> bool:
        return not all(
            self._build_branch(
                InfoMove(cell, option, f"tree search (depth: {self._depth})")
            )
            for option in self._analyzer[cell]
        )

    def _build(self) -> None:
        self._analyzer.apply(self._move)
        if not self._analyzer.check():
            self._no_solution = True
            return
        if self._depth == 1:
            return
        self._analyzer.simplify()
        if not self._analyzer.check():
            self._no_solution = True
            return
        for cell in self._brute_force_order():
            if not self._brute_force_cell(cell):
                self._no_solution = True
                return


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

    def _hard_move(self, analyzer: Analyzer) -> tuple[InfoMove, int] | None:
        for depth in [1, 2, 3]:
            for cell in self._sudoku.empty_cells:
                vals: list[Sudoku.Cell.Option] = []
                for val in analyzer[cell]:
                    if not Tree(analyzer, depth, InfoMove(cell, val)).no_solution:
                        vals.append(val)
                    if len(vals) > 1:
                        break
                if not vals:
                    return
                if len(vals) == 1:
                    return InfoMove(cell, vals[0], "..."), depth

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
            "easy", "medium", "hard", "brute force", "branch-in", "branch-out"
        ],
        move: InfoMove,
    ) -> None:
        if mode == "easy":
            self._complexity += 1
        elif mode == "medium":
            self._complexity += 5
        elif mode == "hard":
            self._complexity += 25
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
