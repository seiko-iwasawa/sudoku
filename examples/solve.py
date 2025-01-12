from pysudoku.solverHuman import SolverHuman
from pysudoku.sudoku import Sudoku


def main():
    hard_sudoku = """\
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
    SolverHuman(sudoku := Sudoku.from_str(hard_sudoku), explain=True).run()
    print(sudoku)


if __name__ == "__main__":
    main()
