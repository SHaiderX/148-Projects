"""CSC148 Assignment 2

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, and Jaisie Sin

=== Module Description ===

This file contains the hierarchy of Goal classes.
"""
from __future__ import annotations
import random
from typing import List, Tuple
from block import Block
from settings import COLOUR_LIST, colour_name


def generate_goals(num_goals: int) -> List[Goal]:
    """Return a randomly generated list of goals with length num_goals.

    All elements of the list must be the same type of goal, but each goal
    must have a different randomly generated colour from COLOUR_LIST. No two
    goals can have the same colour.

    Precondition:
        - num_goals <= len(COLOUR_LIST)
    """
    goals = []
    colors = []
    # Make a copy
    for i in COLOUR_LIST:
        colors.append(i)

    rand = random.randint(0, 1)
    if rand == 1:
        for _unused in range(num_goals):
            x = PerimeterGoal(colors.pop(random.randint(0, len(colors) - 1)))
            goals.append(x)
    else:
        for _unused in range(num_goals):
            x = BlobGoal(colors.pop(random.randint(0, len(colors) - 1)))
            goals.append(x)

    return goals


def _flatten(block: Block) -> List[List[Tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j]

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    L = []
    b = 2 ** (block.max_depth - block.level)
    if len(block.children) == 0:
        for _unused in range(b):
            column = []
            for _i in range(b):
                column.append(block.colour)
            L.append(column)

    else:
        flat1 = _flatten(block.children[0])
        flat2 = _flatten(block.children[1])
        L = flat2 + flat1
        flat3 = _flatten(block.children[2])
        flat4 = _flatten(block.children[3])
        L2 = flat3 + flat4
        for i in range(len(L)):
            L[i].extend(L2[i])

    return L


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class PerimeterGoal(Goal):
    """
    The player must aim to put the most possible units of a given colour c on
    the outer perimeter of the board. The player’s score is the total number of
    unit cells of colour c that are on the perimeter. There is a premium on
    corner cells: they count twice towards the score.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """

    def score(self, board: Block) -> int:
        flat = _flatten(board)
        score = 0
        # checking top and bottom border
        for border in flat:
            if border[0] == self.colour:
                score += 1
            if border[len(flat) - 1] == self.colour:
                score += 1

        # left border
        for left in flat[0]:
            if left == self.colour:
                score += 1

        # right border
        for right in flat[len(flat) - 1]:
            if right == self.colour:
                score += 1

        return score

    def description(self) -> str:
        return ("Perimeter Goal: Fill {}: {} unit circles around the perimeter".
                format(colour_name(self.colour), self.colour))


class BlobGoal(Goal):
    """
    A blob is a group of connected blocks with the same colour.
    Two blocks are connected if their sides touch;
    touching corners doesn’t count. The player’s score is the number of unit
    cells in the largest blob of colour c.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """

    colour: Tuple[int, int, int]

    def score(self, board: Block) -> int:
        _max = 0
        flat = _flatten(board)

        visited = []
        b = 2 ** (board.max_depth - board.level)
        for _unused in range(b):
            column = []
            for _i in range(b):
                column.append(-1)
            visited.append(column)

        for x in range(len(flat)):
            for y in range(len(flat)):
                size = self._undiscovered_blob_size((x, y), flat, visited)
                if size > _max:
                    _max = size

        return _max

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        if pos[0] >= len(board) or pos[1] >= len(board) or \
                pos[0] < 0 or pos[1] < 0:
            return 0

        if board[pos[0]][pos[1]] != self.colour:
            visited[pos[0]][pos[1]] = 0
            return 0

        if visited[pos[0]][pos[1]] == -1:
            size = 1
            visited[pos[0]][pos[1]] = 1
            # top
            size = size + self._undiscovered_blob_size((pos[0], pos[1] - 1),
                                                       board, visited)
            # right
            size = size + self._undiscovered_blob_size((pos[0] + 1, pos[1]),
                                                       board, visited)
            # left
            size = size + self._undiscovered_blob_size((pos[0] - 1, pos[1]),
                                                       board, visited)
            # down
            size = size + self._undiscovered_blob_size((pos[0], pos[1] + 1),
                                                       board, visited)

            return size
        return 0


    def description(self) -> str:
        return ("Blob Goal: Aim to get the largest blob with colour {}: {} ".
                format(colour_name(self.colour), self.colour))


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })
