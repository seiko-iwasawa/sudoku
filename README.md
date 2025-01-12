# Sudoku

## Installation

From source:

```[bash]
pip install .
```

## Description

`SolverStupid` solves sudoku using the backtracking algorithm. Works slow for hard sudoku.

`SolverHuman` solves sudoku like a human. Works very fast.

Usage example in [examples/solve.py](examples/solve.py).

`examples/solve.py` output:

```
[1, 9]->6 (according row has only one occurrence)
.[4, 6]->8 (brute force)
..[2, 6]->1 (brute force)
..[6, 6]->2 (other options are blocked)
..[7, 6]->3 (other options are blocked)
..[2, 5]->3 (according col has only one occurrence)
..[7, 4]->1 (according col has only one occurrence)
...[1, 4]->2 (brute force)
...[3, 3]->2 (according row has only one occurrence)
....[1, 2]->1 (brute force)
<...>
.....[7, 2]->8 (according col has only one occurrence)
.....[9, 6]->5 (according row has only one occurrence)
.....[9, 9]->8 (according row has only one occurrence)
.....[3, 9]->4 (according col has only one occurrence)
.....[3, 8]->3 (other options are blocked)
.....[8, 8]->1 (other options are blocked)
.....[8, 1]->3 (other options are blocked)
.....[9, 1]->1 (other options are blocked)
.....[9, 7]->3 (other options are blocked)
.....[5, 7]->1 (other options are blocked)
.....[7, 9]->2 (other options are blocked)
.....[5, 9]->3 (other options are blocked)
.....[5, 2]->6 (other options are blocked)
.....[5, 8]->2 (other options are blocked)
.....[6, 2]->3 (other options are blocked)
.....[6, 8]->6 (other options are blocked)
.....[7, 6]->1 (other options are blocked)
.....[6, 6]->2 (other options are blocked)
.....[6, 5]->1 (other options are blocked)
.....[7, 5]->3 (other options are blocked)
.....[9, 5]->2 (other options are blocked)
.....[9, 8]->4 (other options are blocked)
╔═══════╦═══════╦═══════╗
║ 4 2 3 ║ 1 5 9 ║ 7 8 6 ║
║ 6 5 7 ║ 8 4 3 ║ 2 9 1 ║
║ 8 9 1 ║ 2 7 6 ║ 5 3 4 ║
╠═══════╬═══════╬═══════╣
║ 2 1 9 ║ 3 6 8 ║ 4 5 7 ║
║ 7 6 8 ║ 5 9 4 ║ 1 2 3 ║
║ 5 3 4 ║ 7 1 2 ║ 8 6 9 ║
╠═══════╬═══════╬═══════╣
║ 9 8 5 ║ 4 3 1 ║ 6 7 2 ║
║ 3 4 2 ║ 6 8 7 ║ 9 1 5 ║
║ 1 7 6 ║ 9 2 5 ║ 3 4 8 ║
╚═══════╩═══════╩═══════╝
```

## TODO

* Sudoku Generator
* Multiple solutions
* SolverAI
