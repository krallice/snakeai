import random
import curses
import time

import abc

from typing import Type, List

from ai import SnakeAI
from core import GameState, Snake, Fruit

class SnakeAIBFS(SnakeAI):

    def __str__(self):
        return 'Breadth First Search - v1'

    def emit_output(self, previous_input: int, gamestate: Type[GameState], snake: Type[Snake], fruit: Type[Fruit]) -> int:
        return previous_input
        