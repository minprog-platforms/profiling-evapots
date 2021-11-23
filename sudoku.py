from __future__ import annotations
from typing import Iterable


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        self._grid: list[str] = []

        for puzzle_row in puzzle:
            row = ""

            for element in puzzle_row:
                row += str(element)

            self._grid.append(row)

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        row = self._grid[y]
        new_row = row[:x] + str(value) + row[x + 1:]
        self._grid[y] = new_row

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        row = self._grid[y]
        new_row = row[:x] + "0" + row[x + 1:]
        self._grid[y] = new_row

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        row = self._grid[y]
        value = int(row[x])

        return value

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""

        # transform row and cols list to set
        col_set = set(self.column_values(x))
        row_set = set(self.row_values(y))

        # transform block list to set
        block_index = (y // 3) * 3 + x // 3
        block_set = set(self.block_values(block_index))

        # find values that are in left as options
        options = list(
            {1, 2, 3, 4, 5, 6, 7, 8, 9} - col_set - row_set - block_set)

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        next_x, next_y = -1, -1

        for y in range(9):
            for x in range(9):
                if self.value_at(x, y) == 0:
                    next_x, next_y = x, y
                    return next_x, next_y

        return next_x, next_y

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""

        # retrieve row from grid and transform to list with integers
        row = self._grid[i]
        values = list(map(int, row))

        return values

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""
        values = []

        for j in range(9):
            values.append(self.value_at(i, j))

        return values

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        values: list[int] = []

        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        for i in range(3):
            row = self._grid[y_start + i]
            values = values + list(map(int, row))[x_start:x_start+3]

        return values

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """

        for i in range(9):
            if len(set(self.column_values(i))) != 9:
                return False
            if len(set(self.row_values(i))) != 9:
                return False
            if len(set(self.block_values(i))) != 9:
                return False

        return True

    def __str__(self) -> str:
        representation = ""

        for row in self._grid:
            representation += row + "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)
