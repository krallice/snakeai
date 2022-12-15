#!/usr/bin/python3

import random
import curses
import time
import sys

import abc

from typing import Type, List

from statistics import *
import pandas as pd
import matplotlib.pyplot as plt

from core import GameState, Snake, Fruit
from ai import SnakeAI
from dummy import SnakeAINull, SnakeAIUp, SnakeAIDirect
from graph import SnakeAIBFS

def gameloop(gamestate: Type[GameState], ai: Type[SnakeAI], snake: Type[Snake], fruit: Type[Fruit], visualise: bool):

    lastpos = []
    key = curses.KEY_RIGHT
    prev_button_direction = None

    # Draw Fruit:
    if visualise == True:
        gamestate.window.addch(fruit.location[0], fruit.location[1], curses.ACS_DIAMOND)

    if visualise == True:
        gamestate.window.border(0)
        gamestate.window.timeout(100)

    while True:

        gamestate.ticks += 1

        # AI Input:
        ai_key = ai.emit_output(key, gamestate, snake, fruit)

        # Get input:
        if visualise == True:
            manual_key = gamestate.window.getch()
            key = manual_key if manual_key != -1 else ai_key
        else:
            key = ai_key

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
            if visualise == True:
                gamestate.window.addch(fruit.location[0], fruit.location[1], curses.ACS_DIAMOND)
        else:
            # Shift the snake along:
            lastpos = snake.shuffle_tail()
            if visualise == True:
                gamestate.window.addch(lastpos[0], lastpos[1], ' ')

        # Render the snake:
        if visualise == True:
            gamestate.window.addch(snake.body[0][0], snake.body[0][1], '#')

        # Collision detection on the boundary:
        if  (snake.head[1] >= (gamestate.screen_width - 1)) or (snake.head[1] <= 0) or \
            (snake.head[0] >= (gamestate.screen_height - 1)) or (snake.head[0] <= 0):
            break

        # Collision detection with self:
        if snake.head in snake.body[1:]:
            break

def map_ai() -> Type[SnakeAI]:
    ai_mapping = { "up": SnakeAIUp, "null": SnakeAINull, "direct": SnakeAIDirect, "bfs": SnakeAIBFS}
    try:
        ai = ai_mapping[sys.argv[1]]() 
    except:
        ai = SnakeAINull()
    return ai

def main():

    # Init our data:
    gamestate = GameState()
    snake = Snake()
    fruit = Fruit()

    # Init our AI:
    ai = map_ai()

    # Setup curses:
    gamestate.init_screen()

    gameloop(gamestate, ai, snake, fruit, True)

    # Cleanup:
    gamestate.cleanup()

    # Stats:
    print("Score: {}".format(gamestate.score))
    print("Snake Length: {}".format(len(snake.body)))
    print("TickCount: {}".format(gamestate.ticks))

def batch_play():

    run_count = 100
    run_stats = []

    # Init our AI:
    ai = map_ai()
    
    # Run Games:
    for n in range(1, run_count):

        # Init our data:
        gamestate = GameState()
        snake = Snake()
        fruit = Fruit()

        # Setup curses:
        gamestate.init_screen(False)
        gameloop(gamestate, ai, snake, fruit, False)
        run_stats.append({"Score": gamestate.score, "Ticks": gamestate.ticks})
    
    # Games finished, print summary:
    print(f"AI: {ai}\nRuns: {run_count}")
    print(f"- - -")

    scores = [r["Score"] for r in run_stats]
    q = quantiles(scores, n=100)

    print(f"Average Score: {round(mean(scores), 2)}")

    print(f"p1: {q[0]}")
    print(f"p5: {q[4]}")
    print(f"p10: {q[9]}")
    print(f"p25: {q[24]}")
    print(f"Median(p50): {median(scores)}")
    print(f"p75: {q[74]}")
    print(f"p90: {q[89]}")
    print(f"p95: {q[94]}")
    print(f"p99: {q[98]}")

    counts = pd.Series(scores).value_counts().sort_index().plot(kind='bar')
    plt.title(f"AI: {ai}\nRuns: {run_count}")
    plt.ylabel("Game Count")
    plt.xlabel("Game Score")
    plt.savefig('x.png')

if __name__ == '__main__':
    # main()
    batch_play()