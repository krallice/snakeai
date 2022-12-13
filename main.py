#!/usr/bin/python3

import random
import curses
import time
import sys

import abc

from typing import Type, List

from core import GameState, Snake, Fruit
from ai import SnakeAI
from dummy import SnakeAINull, SnakeAIUp, SnakeAIDirect

def gameloop(gamestate: Type[GameState], ai: Type[SnakeAI], snake: Type[Snake], fruit: Type[Fruit]):

    # Draw Fruit:
    gamestate.window.addch(fruit.location[0], fruit.location[1], curses.ACS_DIAMOND)

    lastpos = []
    key = curses.KEY_RIGHT
    prev_button_direction = None

    while True:

        gamestate.window.border(0)
        gamestate.window.timeout(100)

        gamestate.ticks += 1

        # AI Input:
        ai_key = ai.emit_output(key, gamestate, snake, fruit)

        # Get input:
        manual_key = gamestate.window.getch()
        key = manual_key if manual_key != -1 else ai_key

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

    # Init our AI:
    ai_mapping = { "up": SnakeAIUp, "null": SnakeAINull, "direct": SnakeAIDirect}
    try:
        ai = ai_mapping[sys.argv[1]]() 
    except:
        ai = SnakeAINull()

    # Setup curses:
    gamestate.init_screen()

    gameloop(gamestate, ai, snake, fruit)

    # Cleanup:
    gamestate.cleanup()

    # Stats:
    print("Score: {}".format(gamestate.score))
    print("Snake Length: {}".format(len(snake.body)))
    print("TickCount: {}".format(gamestate.ticks))

if __name__ == '__main__':
    main()