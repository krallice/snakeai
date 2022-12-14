import random
import curses
import time

import abc

import sys

from collections import deque

from typing import Type, List

from ai import SnakeAI
from core import GameState, Snake, Fruit

class SnakeAIBFS(SnakeAI):

    def __str__(self):
        return 'Breadth First Search - v1'

    def emit_output(self, previous_input: int, gamestate: Type[GameState], snake: Type[Snake], fruit: Type[Fruit]) -> int:
        
        bfs_queue = deque()
        
        # Map each node to a True/False value indicating if the node has already been added to the queue:
        node_visited_list = []

        # Used to trackback from the fruit all the way back to the head to determine the next direction to take:
        parent_path = {}

        # Clockwise pattern:    UP      RIGHT    DOWN    LEFT
        # Used for building the bfs queue:
        traversal_pattern = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        incompatible_direction = [curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_RIGHT]

        next_input_key = [curses.KEY_UP, curses.KEY_RIGHT, curses.KEY_DOWN, curses.KEY_LEFT]

        # Start at the head:
        bfs_queue.append(snake.head)
        node_visited_list.append(snake.head)

        fruit_found_flag = False

        # BFS Loop:
        while (len(bfs_queue) > 0):

            current_node = bfs_queue.popleft()

            # We've found our fruit?
            if current_node == fruit.location:
                fruit_found_flag = True
                break
            
            # In a clockwise direction, explore the grid, adding nodes to our queue:
            for i, traversal_direction in enumerate(traversal_pattern):
                
                # Account for the fact that the snake cannot 180 reverse in-line:
                if ((current_node == snake.head) and (previous_input == incompatible_direction[i])):
                    continue

                # Candidate node to check:
                candidate = [current_node[0] + traversal_direction[0], current_node[1] + traversal_direction[1]]

                # Check if we are out of bounds:
                if ((candidate[0] < 1) or (candidate[0] > gamestate.screen_height - 2) or \
                    (candidate[1] < 1) or (candidate[1] > gamestate.screen_width - 2)):
                    continue

                # Check if we are a snake tail:
                if (candidate in snake.body):
                    continue

                # By this stage: we should be good to add the node to our queue.
                # Record the parent path so we can walk all the way back from the fruit back to the snake once we exit the loop:
                if (candidate not in node_visited_list):
                    node_visited_list.append(candidate)
                    parent_path[str(candidate)] = current_node
                    bfs_queue.append(candidate)

        # If we didnt find the fruit, that means the area has been bisected by the snake's tail.
        # Lazy logic for now, but just keep going:
        if (fruit_found_flag == False):
            return previous_input

        # Walk the path backwards to get the next node the snake must enter:
        path_node = fruit.location
        while path_node != snake.head:
            last_path_node = path_node
            path_node = parent_path.get(str(path_node), snake.head)

        # Calculate Delta
        delta_direction = [0, 0]
        delta_direction[0] = last_path_node[0] - snake.head[0]
        delta_direction[1] = last_path_node[1] - snake.head[1]

        try:
            return_val = next_input_key[traversal_pattern.index(delta_direction)]
        except ValueError:
            print(f"SNAKE HEAD: {snake.head}")
            print(f"FRUIT: {fruit.location}")
            print(f"LAST PATH NODE: {last_path_node}")
            print(f"DELTA DIRECTION: {delta_direction}")

            sys.exit

        return return_val
