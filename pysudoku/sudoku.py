from collections.abc import Generator, Iterable


class Sudoku:

    N = 9
    """sudoku size"""
    B = 3
    """sudoku block size"""

    class Cell:

        class Option:

            def __init__(self, val: int = 0) -> None:
                if not (0 <= val <= Sudoku.N):
                    raise ValueError(f"incorrect cell option: {val}")
                self._val = val

            @classmethod
            def from_str(cls, val: str) -> "Sudoku.Cell.Option":
                try:
                    return cls(0 if val == "." else int(val))
                except Exception:
                    raise ValueError(f"incorrect cell option: {val}")

            def __int__(self) -> int:
                return self._val

            def __str__(self) -> str:
                return str(self._val) if self._val else "."

            def __repr__(self) -> str:
                return f"Option(_val={self._val})"

            def __bool__(self) -> bool:
                return self.filled()

            def __eq__(self, value: object) -> bool:
                return isinstance(value, Sudoku.Cell.Option) and self._val == value._val

            def __hash__(self) -> int:
                return hash(self._val)

            def empty(self) -> bool:
                return self._val == 0

            def filled(self) -> bool:
                return self._val != 0

            @staticmethod
            def all() -> Generator["Sudoku.Cell.Option"]:
                yield from map(Sudoku.Cell.Option, range(1, Sudoku.N + 1))

        def __init__(self, row: int, col: int, val: Option | None = None) -> None:
            self._row = row
            self._col = col
            self._val = val or Sudoku.Cell.Option()

        @property
        def row(self) -> int:
            return self._row

        @property
        def col(self) -> int:
            return self._col

        @property
        def block(self) -> int:
            return self.row // Sudoku.B * Sudoku.B + self.col // Sudoku.B

        @property
        def val(self) -> Option:
            return self._val

        @val.setter
        def val(self, new_val: Option) -> None:
            if self.val.filled():
                raise ValueError("cell is already filled")
            self._val = new_val

        def reset(self) -> None:
            self._val = Sudoku.Cell.Option()

        def empty(self) -> bool:
            return self.val.empty()

        def filled(self) -> bool:
            return self.val.filled()

        def __str__(self) -> str:
            return f"[{self.row + 1}, {self.col + 1}]" + (
                f"-{self.val}" if self.val else ""
            )

        def __repr__(self) -> str:
            return f"Cell(row={self.row}, col={self.col}, val={int(self.val)})"

    @staticmethod
    def is_related(cell: Cell, other: Cell) -> bool:
        return (
            cell.row == other.row or cell.col == other.col or cell.block == other.block
        )

    type Row = list[Cell]
    type Col = list[Cell]
    type Block = list[Cell]

    def __init__(self) -> None:
        self._grid = [
            [Sudoku.Cell(i, j) for j in range(Sudoku.N)] for i in range(Sudoku.N)
        ]

    @classmethod
    def from_iter(cls, iter: Iterable["Sudoku.Cell.Option"]) -> "Sudoku":
        res = cls()
        for cell, val in zip(res.cells, iter):
            cell.val = val
        return res

    @classmethod
    def from_grid(cls, grid: list[list[int]]) -> "Sudoku":
        if len(grid) != Sudoku.N or any(len(row) != Sudoku.N for row in grid):
            raise ValueError("incorrect grid shape")
        return cls.from_iter(Sudoku.Cell.Option(val) for row in grid for val in row)

    @classmethod
    def from_str(cls, s: str) -> "Sudoku":
        return cls.from_iter(
            map(Sudoku.Cell.Option.from_str, filter(lambda c: c in ".0123456789", s))
        )

    @classmethod
    def from_input(cls) -> "Sudoku":

        def set_val():
            try:
                sudoku[i][j].val = Sudoku.Cell.Option.from_str(val)
            except Exception:
                print(f"warning: incorrect cell {Sudoku.Cell(i, j)}-{val}")

        sudoku = Sudoku()
        for i in range(Sudoku.N):
            for j, val in enumerate(input()):
                set_val()
        return sudoku

    def __getitem__(self, ind: int) -> Row:
        return self._grid[ind]

    def __str__(self) -> str:
        return """\
╔═══════╦═══════╦═══════╗
║ {}{}{}║ {}{}{}║ {}{}{}║
║ {}{}{}║ {}{}{}║ {}{}{}║
║ {}{}{}║ {}{}{}║ {}{}{}║
╠═══════╬═══════╬═══════╣
║ {}{}{}║ {}{}{}║ {}{}{}║
║ {}{}{}║ {}{}{}║ {}{}{}║
║ {}{}{}║ {}{}{}║ {}{}{}║
╠═══════╬═══════╬═══════╣
║ {}{}{}║ {}{}{}║ {}{}{}║
║ {}{}{}║ {}{}{}║ {}{}{}║
║ {}{}{}║ {}{}{}║ {}{}{}║
╚═══════╩═══════╩═══════╝""".format(
            *(str(cell.val) + " " for cell in self.cells)
        )

    def __repr__(self) -> str:
        return f"Sudoku(_grid={[[int(cell.val) for cell in row] for row in self]})"

    def cell(self, i: int, j: int) -> Cell:
        return self[i][j]

    @property
    def cells(self) -> Generator[Cell]:
        return (cell for row in self for cell in row)

    @property
    def empty_cells(self) -> Generator[Cell]:
        return (cell for cell in self.cells if cell.empty())

    @property
    def filled_cells(self) -> Generator[Cell]:
        return (cell for cell in self.cells if cell.filled())

    def row(self, i: int) -> Row:
        return self[i]

    @property
    def rows(self) -> Generator[Row]:
        return (row for row in self)

    def col(self, j: int) -> Col:
        return [self[i][j] for i in range(Sudoku.N)]

    @property
    def cols(self) -> Generator[Row]:
        return (self.col(j) for j in range(Sudoku.N))

    def block(self, b: int) -> Block:
        x = b // Sudoku.B * Sudoku.B
        y = b % Sudoku.B * Sudoku.B
        return [self[i + x][j + y] for i in range(Sudoku.B) for j in range(Sudoku.B)]

    @property
    def blocks(self) -> Generator[Block]:
        return (self.block(b) for b in range(Sudoku.N))

    def related_cells(self, cell: Cell) -> Generator[Cell]:
        yield from filter(
            lambda rel_cell: rel_cell.block != cell.block, self.row(cell.row)
        )
        yield from filter(
            lambda rel_cell: rel_cell.block != cell.block, self.col(cell.col)
        )
        yield from filter(lambda rel_cell: rel_cell != cell, self.block(cell.block))

    def related_empty_cells(self, cell: Cell) -> Generator[Cell]:
        return (cell for cell in self.related_cells(cell) if cell.empty())

    def related_filled_cells(self, cell: Cell) -> Generator[Cell]:
        return (cell for cell in self.related_cells(cell) if cell.filled())

    def conflict(self) -> tuple[Cell, Cell] | None:
        for cell1 in self.filled_cells:
            for cell2 in self.related_filled_cells(cell1):
                if cell1.val == cell2.val:
                    return cell1, cell2
        return None

    def is_correct(self) -> bool:

        def all_are_unique(cells: list[Sudoku.Cell]):
            options = [cell.val for cell in cells if cell.filled()]
            return len(set(options)) == len(options)

        return all(
            all_are_unique(cells)
            for groups in [self.rows, self.cols, self.blocks]
            for cells in groups
        )

    def empty(self) -> bool:
        return all(cell.empty() for cell in self.cells)

    def filled(self) -> bool:
        return all(cell.filled() for cell in self.cells)

    def clear(self) -> None:
        for cell in self.filled_cells:
            cell.reset()
