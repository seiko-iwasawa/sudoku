import time

from pysudoku.solver import SolverHuman, SolverStupid
from pysudoku.sudoku import Sudoku

easy_sudoku = """\
.642973..
27953....
.8......7
51..628..
9......6.
6.784....
...174925
49.....86
7526894.3"""

medium_sudoku = """\
7.98..54.
...7.....
6...4..2.
..46...59
..6...7..
51...48..
.4..8...5
.....6...
.67..59.2"""

hard_sudoku = """\
....5978.
6.....29.
.9..76...
2.93..4.7
7.8594...
...7..8.9
..5....7.
.4.6.....
...9....."""


def speedtest(f, name):
    start = time.process_time()
    f()
    end = time.process_time()
    print(f"{name} time:\t{(end - start)}")


def main():
    speedtest(SolverStupid(Sudoku.from_str(easy_sudoku)).run, "stupid+easy")
    speedtest(SolverStupid(Sudoku.from_str(medium_sudoku)).run, "stupid+medium")
    speedtest(SolverStupid(Sudoku.from_str(hard_sudoku)).run, "stupid+hard")
    print("===")
    speedtest(SolverHuman(Sudoku.from_str(easy_sudoku)).run, "human+easy")
    speedtest(SolverHuman(Sudoku.from_str(medium_sudoku)).run, "human+medium")
    speedtest(SolverHuman(Sudoku.from_str(hard_sudoku)).run, "human+hard")


if __name__ == "__main__":
    main()
