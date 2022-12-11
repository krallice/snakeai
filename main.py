#!/usr/bin/python3

import random
import curses
import time

from typing import Type, List

class GameState(object):

    def __init__(self):
        self.score = 0

    def init_screen(self):

        # Initialise our screen:
        self.screen = curses.initscr()
        self.screen_height, self.screen_width = self.screen.getmaxyx()
        self.window = curses.newwin(self.screen_height, self.screen_width, 0, 0)

        self.window.keypad(1)
        curses.curs_set(0)

class Snake(object):

    def __init__(self):

        # (Y, X) from Origin == Top Left
        self.head = [15,160]
        self.body = [[15,160],[15,159],[15,158]]
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
        self.location = [15,175]

    def newlocation(self, snake_positions: List[List], screen_height: int, screen_width: int):

        candidate_position = [0, 0]
        while True:
            candidate_position = [random.randint(1, screen_height - 2), random.randint(1, screen_width - 2)]
            if candidate_position not in snake_positions:
                break
        self.location = candidate_position

def gameloop(gamestate: Type[GameState], snake: Type[Snake], fruit: Type[Fruit]):

    # Draw Fruit:
    gamestate.window.addch(fruit.location[0], fruit.location[1], curses.ACS_DIAMOND)

    lastpos = []
    key = curses.KEY_RIGHT
    prev_button_direction = None

    while True:

        gamestate.window.border(0)
        gamestate.window.timeout(100)

        # Get input:
        next_key = gamestate.window.getch()
        key = next_key if next_key != -1 else key

        # Validate input:
        if key == curses.KEY_LEFT and prev_button_direction != curses.KEY_RIGHT:
            button_direction = curses.KEY_LEFT
        elif key == curses.KEY_RIGHT and prev_button_direction != curses.KEY_LEFT:
            button_direction = curses.KEY_RIGHT
        elif key == curses.KEY_UP and prev_button_direction != curses.KEY_DOWN:
            button_direction = curses.KEY_UP
        elif key == curses.KEY_DOWN and prev_button_direction != curses.KEY_UP:
            button_direction = curses.KEY_DOWN
        else:
            pass

        prev_button_direction = button_direction

        # Move the snake:
        if button_direction == curses.KEY_LEFT:
            snake.velocity = [0, -1]
        elif button_direction == curses.KEY_RIGHT:
            snake.velocity = [0, 1]
        elif button_direction == curses.KEY_UP:
            snake.velocity = [-1, 0]
        elif button_direction == curses.KEY_DOWN:
            snake.velocity = [1, 0]

        snake.move()

        # Detect if the snake eats the fruit:
        if ((snake.head[0] == fruit.location[0]) and (snake.head[1] == fruit.location[1])):
            gamestate.score += 1
            fruit.newlocation(snake.body, gamestate.screen_height, gamestate.screen_width)
            gamestate.window.addch(fruit.location[0], fruit.location[1], curses.ACS_DIAMOND)
        else:
            # Shift the snake along:
            lastpos = snake.shuffle_tail()
            gamestate.window.addch(lastpos[0], lastpos[1], ' ')

        # Render the snake:
        gamestate.window.addch(snake.body[0][0], snake.body[0][1], '#')

        # Collision detection on the boundary:
        if  (snake.head[1] >= (gamestate.screen_width - 1)) or (snake.head[1] <= 0) or \
            (snake.head[0] >= (gamestate.screen_height - 1)) or (snake.head[0] <= 0):
            break

        # Collision detection with self:
        if snake.head in snake.body[1:]:
            break

def main():

    # Init our data:
    gamestate = GameState()
    snake = Snake()
    fruit = Fruit()

    # Setup curses:
    gamestate.init_screen()

    gameloop(gamestate, snake, fruit)

    # Cleanup:
    gamestate.screen.refresh()
    curses.endwin()

if __name__ == '__main__':
    main()