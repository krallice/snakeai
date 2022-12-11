import random
import curses
import time

import abc

from typing import Type, List

from core import GameState, Snake, Fruit

class SnakeAI(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def emit_output(self, previous_input: int, gamestate: Type[GameState], snake: Type[Snake], fruit: Type[Fruit]) -> int:
        raise NotImplementedError()
