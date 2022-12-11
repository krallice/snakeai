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