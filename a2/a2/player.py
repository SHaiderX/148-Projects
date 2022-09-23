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
Misha Schwartz, and Jaisie Sin.

=== Module Description ===

This file contains the hierarchy of player classes.
"""
from __future__ import annotations
from typing import List, Optional, Tuple
import random
import pygame

from block import Block
from goal import Goal, generate_goals

from actions import KEY_ACTION, ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE, \
    SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, PASS, PAINT, COMBINE


def create_players(num_human: int, num_random: int, smart_players: List[int]) \
        -> List[Player]:
    """Return a new list of Player objects.

    <num_human> is the number of human player, <num_random> is the number of
    random players, and <smart_players> is a list of difficulty levels for each
    SmartPlayer that is to be created.

    The list should contain <num_human> HumanPlayer objects first, then
    <num_random> RandomPlayer objects, then the same number of SmartPlayer
    objects as the length of <smart_players>. The difficulty levels in
    <smart_players> should be applied to each SmartPlayer object, in order.
    """
    out = []
    goals = generate_goals(num_random + num_human + len(smart_players))
    for i in range(num_human):
        out.append(HumanPlayer(i, goals[i]))

    for i in range(num_random):
        out.append(RandomPlayer(num_human + i, goals[num_human + i]))

    for i in range(len(smart_players)):
        out.append(SmartPlayer(num_human + num_random + i,
                               goals[num_human + num_random + i],
                               smart_players[i]))

    return out


# Helpers


def _collapse(block: Block) -> List[Block]:
    """_collapse the structure of the block into a list
    Helper function
    """
    if len(block.children) == 0:
        return [block]
    else:
        lst = [block]
        for child in block.children:
            lst += _collapse(child)
        return lst


def _ran_node(block: Block) -> Block:
    """return a random block in the block
     Helper function
    """
    lst = _collapse(block)
    return lst[random.randint(0, len(lst) - 1)]


def _has_coords(block: Block, location: Tuple[int, int]) -> bool:
    """
    Return a Boolean value based on if location is in side the premise of Block.
    """
    pos = block.position
    max_pos = (pos[0] + block.size, pos[1] + block.size)
    if location[0] < max_pos[0] and location[1] < max_pos[1]:
        if location[0] >= pos[0] and location[1] >= pos[1]:
            return True
    return False


def _get_block(block: Block, location: Tuple[int, int], level: int) -> \
        Optional[Block]:
    """Return the Block within <block> that is at <level> and includes
    <location>. <location> is a coordinate-pair (x, y).

    A block includes all locations that are strictly inside of it, as well as
    locations on the top and left edges. A block does not include locations that
    are on the bottom or right edge.

    If a Block includes <location>, then so do its ancestors. <level> specifies
    which of these blocks to return. If <level> is greater than the level of
    the deepest block that includes <location>, then return that deepest block.

    If no Block can be found at <location>, return None.

    Preconditions:
        - 0 <= level <= max_depth
    """
    if block.level == level and _has_coords(block, location):
        return block
    else:
        for child in block.children:
            n = _get_block(child, location, level)
            if n is not None:
                return n
    return None


def _valid_move(board: Block, move: Tuple[str, Optional[int]],
                color: Tuple[int, int, int]) -> bool:
    """checks if the move is legal on the block.
    Helper Function
    """
    boo = False
    if move == ROTATE_COUNTER_CLOCKWISE:
        boo = board.rotate(3)
    elif move == ROTATE_CLOCKWISE:
        boo = board.rotate(1)
    elif move == SWAP_HORIZONTAL:
        boo = board.swap(0)
    elif move == SWAP_VERTICAL:
        boo = board.swap(1)
    elif move == SMASH:
        boo = board.smash()
    elif move == COMBINE:
        boo = board.combine
    elif move == PAINT:
        boo = board.paint(color)

    return boo


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    id:
        This player's number.
    goal:
        This player's assigned goal for the game.
    """
    id: int
    goal: Goal

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.id = player_id

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player.

        If no block is selected by the player, return None.
        """
        raise NotImplementedError

    def process_event(self, event: pygame.event.Event) -> None:
        """Update this player based on the pygame event.
        """
        raise NotImplementedError

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a potential move to make on the game board.

        The move is a tuple consisting of a string, an optional integer, and
        a block. The string indicates the move being made (i.e., rotate, swap,
        or smash). The integer indicates the direction (i.e., for rotate and
        swap). And the block indicates which block is being acted on.

        Return None if no move can be made, yet.
        """
        raise NotImplementedError


def _create_move(action: Tuple[str, Optional[int]], block: Block) -> \
        Tuple[str, Optional[int], Block]:
    return action[0], action[1], block


class HumanPlayer(Player):
    """A human player.

    === Private Attributes ===
    _level:
        The level of the Block that the user selected most recently.
    _desired_action:
        The most recent action that the user is attempting to do.

    == Representation Invariants concerning the private attributes ==
        _level >= 0
    """
    _level: int
    _desired_action: Optional[Tuple[str, Optional[int]]]

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        Player.__init__(self, player_id, goal)

        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._desired_action = None

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player based on
        the position of the mouse on the screen and the player's desired level.

        If no block is selected by the player, return None.
        """
        mouse_pos = pygame.mouse.get_pos()
        block = _get_block(board, mouse_pos, self._level)

        return block

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the relevant keyboard events made by the player based on
        the mapping in KEY_ACTION, as well as the W and S keys for changing
        the level.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in KEY_ACTION:
                self._desired_action = KEY_ACTION[event.key]
            elif event.key == pygame.K_w:
                self._level = max(0, self._level - 1)
                self._desired_action = None
            elif event.key == pygame.K_s:
                self._level += 1
                self._desired_action = None

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return the move that the player would like to perform. The move may
        not be valid.

        Return None if the player is not currently selecting a block.
        """
        block = self.get_selected_block(board)

        if block is None or self._desired_action is None:
            return None
        else:
            move = _create_move(self._desired_action, block)

            self._desired_action = None
            return move


class RandomPlayer(Player):
    """
    A computer controller player that randomly makes moves

    === Private Attributes ===
    _proceed:
      True when the player should make a move, False when the player should
      wait.
    """
    _proceed: bool

    def __init__(self, player_id: int, goal: Goal) -> None:
        Player.__init__(self, player_id, goal)
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid, randomly generated move.

        A valid move is a move other than PASS that can be successfully
        performed on the <board>.

        This function does not mutate <board>.

        list of moves: combine, paint, rotate, swap, smash

                    # if ran_move[-1] is None:
            #     boo = getattr(ran_block, ran_move[0])
            # else:
            #     boo = getattr(ran_block, ran_move[0])(ran_move[1])
        """

        if not self._proceed:
            return None  # Do not remove

        else:
            movelist = [ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE,
                        SWAP_HORIZONTAL,
                        SWAP_VERTICAL, SMASH, COMBINE, PAINT]
            ran_move = movelist[random.randint(0, len(movelist) - 1)]

            new_block = board.create_copy()

            ran_block = _ran_node(new_block)

            boo = _valid_move(ran_block, ran_move, self.goal.colour)

            if not boo:
                self.generate_move(board)
            else:
                self._proceed = False
                loc = ran_block.position
                lev = ran_block.level

                out = _get_block(board, loc, lev)

                return ran_move[0], ran_move[-1], out

        self._proceed = False  # Must set to False before returning!
        return None


class SmartPlayer(Player):
    """
    A computer player that chooses moves more intelligently:
    It generates a set of random moves and, for each move, checks what
    its score would be if it were to make that move. Then it picks the one
    that yields the best score.

    === Private Attributes ===
    _proceed:
      True when the player should make a move, False when the player should
      wait.
    """
    _proceed: bool
    difficulty: int

    def __init__(self, player_id: int, goal: Goal, difficulty: int) -> None:
        Player.__init__(self, player_id, goal)
        self._proceed = False
        self.difficulty = difficulty

    def get_selected_block(self, board: Block) -> Optional[Block]:
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid move by assessing multiple valid moves and choosing
        the move that results in the highest score for this player's goal (i.e.,
        disregarding penalties).

        A valid move is a move other than PASS that can be successfully
        performed on the <board>. If no move can be found that is better than
        the current score, this player will pass.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None  # Do not remove

        else:
            lst_randoms = []
            for i in range(self.difficulty):
                new_boards = helper_random(board, self.goal)
                lst_randoms.append(new_boards)

            max_score = self.goal.score(board)
            max_idx = 0
            for i in range(len(lst_randoms)):

                s = self.goal.score(lst_randoms[i][0])
                if s >= max_score:
                    max_score = s
                    max_idx = i

            if max_score == self.goal.score(board):
                self._proceed = False
                return PASS[0], PASS[1], board

            loc = lst_randoms[max_idx][1].position
            lev = lst_randoms[max_idx][1].level
            out = _get_block(board, loc, lev)

            self._proceed = False
            return lst_randoms[max_idx][2][0], lst_randoms[max_idx][2][1], out


def helper_random(board: Block, goal: Goal) -> \
        Tuple[Block, Block, Tuple[str, Optional[int]]]:
    """
    Return a new block with a random move applied to a random node within the
    block.
    Helper Function
    """
    boo = False
    new_block = board.create_copy()
    ran_block = _ran_node(new_block)
    movelist = [ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE,
                SWAP_HORIZONTAL,
                SWAP_VERTICAL, SMASH, COMBINE, PAINT]
    ran_move = movelist[random.randint(0, len(movelist) - 1)]

    while not boo:
        ran_move = movelist[random.randint(0, len(movelist) - 1)]

        new_block = board.create_copy()
        ran_block = _ran_node(new_block)
        boo = _valid_move(ran_block, ran_move, goal.colour)

    return new_block, ran_block, ran_move


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'actions', 'block',
            'goal', 'pygame', '__future__'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
