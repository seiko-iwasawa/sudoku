from pysudoku.solver import SolverHuman
from pysudoku.sudoku import Sudoku


def main():
    sudoku = Sudoku.from_input()
    SolverHuman(sudoku).run()
    print(sudoku)


if __name__ == "__main__":
    main()
