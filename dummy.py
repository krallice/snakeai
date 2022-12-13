import random
import curses
import time

import abc

from typing import Type, List

from ai import SnakeAI
from core import GameState, Snake, Fruit

class SnakeAINull(SnakeAI):

    def emit_output(self, previous_input: int, gamestate: Type[GameState], snake: Type[Snake], fruit: Type[Fruit]) -> int:
        return previous_input

class SnakeAIUp(SnakeAI):

    def emit_output(self, previous_input: int, gamestate: Type[GameState], snake: Type[Snake], fruit: Type[Fruit]) -> int:
        return curses.KEY_UP

class SnakeAIDirect(SnakeAI):

    """ Direct Path Solver

    Solves for the X Axis first. Once the head is aligned to the same X axis as the fruit,
    the snake pivots to solve for Y.

    No collision detection logic.
    
    """

    def emit_output(self, previous_input: int, gamestate: Type[GameState], snake: Type[Snake], fruit: Type[Fruit]) -> int:
        
        if previous_input == curses.KEY_RIGHT:
            # Keep solving for X:
            if fruit.location[1] < snake.head[1]:
                if snake.head[0] > (gamestate.screen_height / 2):
                    return curses.KEY_UP
                else:
                    return curses.KEY_DOWN
            elif fruit.location[1] > snake.head[1]:
                return previous_input
            # X is solved, now solve for Y:
            elif fruit.location[1] == snake.head[1]:
                if fruit.location[0] < snake.head[0]:
                    return curses.KEY_UP
                else:
                    return curses.KEY_DOWN

        elif previous_input == curses.KEY_UP or previous_input == curses.KEY_DOWN:
            # Pivot:
            if fruit.location[1] < snake.head[1]:
                return curses.KEY_LEFT
            elif fruit.location[1] > snake.head[1]:
                return curses.KEY_RIGHT
            # X is solved, now solve for Y:
            else:
                return previous_input

        elif previous_input == curses.KEY_LEFT:
            # Keep solving for X:
            if fruit.location[1] < snake.head[1]:
                return previous_input
            elif fruit.location[1] > snake.head[1]:
                if snake.head[0] > (gamestate.screen_height / 2):
                    return curses.KEY_UP
                else:
                    return curses.KEY_DOWN
            # X is solved, now solve for Y:
            elif fruit.location[1] == snake.head[1]:
                if fruit.location[0] < snake.head[0]:
                    return curses.KEY_UP
                else:
                    return curses.KEY_DOWN
