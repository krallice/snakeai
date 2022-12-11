import random
import curses
import time

import abc

from typing import Type, List

class GameState(object):

    def __init__(self):
        self.score = 0
        self.ticks = 0

    def init_screen(self):

        # Initialise our screen:
        self.screen = curses.initscr()
        # self.screen_height, self.screen_width = self.screen.getmaxyx()
        self.screen_height = 20
        self.screen_width = 20
        self.window = curses.newwin(self.screen_height, self.screen_width, 0, 0)

        self.window.keypad(1)
        curses.curs_set(0)

class Snake(object):

    def __init__(self):

        # (Y, X) from Origin == Top Left
        self.head = [15,15]
        self.body = [[15,15],[15,14],[15,13]]
        self.velocity = [0, 1]

    def move(self):

        self.head[0] += self.velocity[0]
        self.head[1] += self.velocity[1]

        self.body.insert(0, list(self.head))

        # return self.body.pop()
        #return None
        return

    def shuffle_tail(self):
        return self.body.pop()

class Fruit(object):

    def __init__(self):
        self.location = [5,5]

    def newlocation(self, snake_positions: List[List], screen_height: int, screen_width: int):

        candidate_position = [0, 0]
        while True:
            candidate_position = [random.randint(1, screen_height - 2), random.randint(1, screen_width - 2)]
            if candidate_position not in snake_positions:
                break
        self.location = candidate_position
