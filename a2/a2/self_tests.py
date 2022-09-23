from typing import List, Optional, Tuple
import os
import pygame
import pytest

from block import Block
from blocky import _block_to_squares
from goal import BlobGoal, PerimeterGoal, _flatten
from player import _get_block
from renderer import Renderer

COLOUR_LIST = [0, 1, 2, 3]

def set_children(block: Block, colours: List[Optional[Tuple[int, int, int]]]) \
        -> None:
    """Set the children at <level> for <block> using the given <colours>.

    Precondition:
        - len(colours) == 4
        - block.level + 1 <= block.max_depth
    """
    size = block._child_size()
    positions = block._children_positions()
    level = block.level + 1
    depth = block.max_depth

    block.children = []  # Potentially discard children
    for i in range(4):
        b = Block(positions[i], size, colours[i], level, depth)
        block.children.append(b)

def board_16x16() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 2.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[0], colours)

    return board

    # def _blob_size_helper(self, x: int, y: int,
    #                       board: List[List[Tuple[int, int, int]]],
    #                       visited: List[List[int]]) -> int:
    #     """A helper function that returns the largest blob of unvisited
    #     blocks depending on the x and y of of the block
    #     """
    #     if x >= len(visited) or y >= len(visited) or \
    #             x < 0 or y < 0:
    #         return 0
    #
    #     if visited[x][y] == -1:
    #         if board[x][y] == self.colour:
    #             visited[x][y] = 1
    #             return 1 + self._undiscovered_blob_size((x, y), board, visited)
    #         else:
    #             visited[x][y] = 0
    #             return 0
    #     return 0

visited = []
b = 2 ** (board_16x16().max_depth - board_16x16().level)
for _unused in range(b):
    column = []
    for _i in range(b):
        column.append(-1)
    visited.append(column)


# Level 0
board_16x16_swap0 = Block((0, 0), 750, None, 0, 2)
# Level 1
colours = [COLOUR_LIST[2], None, COLOUR_LIST[3], COLOUR_LIST[1]]
set_children(board_16x16_swap0, colours)
# Level 2
colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
set_children(board_16x16_swap0.children[1], colours)

board_16x16r = board_16x16().create_copy()
board_16x16r.children[0].rotate(1)



def board_16x16_rotate1() -> Block:
    """Create a reference board where the top-right block on level 1 has been
    rotated clockwise.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[0]]
    set_children(board.children[0], colours)

    return board
