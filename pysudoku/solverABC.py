from abc import ABC, abstractmethod
from collections.abc import Generator

from pysudoku.move import Move
from pysudoku.sudoku import Sudoku


class SolverABC(ABC):
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
