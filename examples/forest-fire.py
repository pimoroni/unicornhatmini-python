#!/usr/bin/env python3

# Forest fire model cellular automaton. Simulates the growth
# of trees in a forest, with sporadic outbreaks of forest fires.

# https://en.wikipedia.org/wiki/Forest-fire_model

# Based on Rosetta Code Python Forest Fire example.
# https://rosettacode.org/wiki/Forest_fire#Python

import random
import time

from unicornhatmini import UnicornHATMini

print("""
Unicorn HAT Mini: forest-fire.py

Forest fire model cellular automaton. Simulates the growth
of trees in a forest, with sporadic outbreaks of forest fires.

Press Ctrl+C to exit!
""")


# Avoid retina-searage!
unicornhatmini = UnicornHATMini()
unicornhatmini.set_brightness(0.1)
unicornhatmini.set_rotation(0)

# The height and width of the forest.
width, height = unicornhatmini.get_shape()

# Initial probability of a grid square having a tree
initial_trees = 0.55

# p = probability of tree growing, f = probability of fire
p = 0.01
f = 0.0005

# Brightness values for a tree, fire, and blank space
tree = [0, 255, 0]
burning = [255, 0, 0]
space = [0, 0, 0]

# Each square's neighbour coordinates
hood = ((-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1))


# Function to populate the initial forest
def initialise():
    grid = {(x, y): (tree if random.random() <= initial_trees else space) for x in range(width) for y in range(height)}
    return grid


# Display the forest, in its current state, on UnicornHATMini
def show_grid(grid):
    unicornhatmini.clear()
    for x in range(width):
        for y in range(height):
            unicornhatmini.set_pixel(x, y, *grid[(x, y)])
    unicornhatmini.show()


# Go through grid, update grid squares based on state of
# square and neighbouring squares
def update_grid(grid):
    new_grid = {}
    for x in range(width):
        for y in range(height):
            if grid[(x, y)] == burning:
                new_grid[(x, y)] = space
            elif grid[(x, y)] == space:
                new_grid[(x, y)] = tree if random.random() <= p else space
            elif grid[(x, y)] == tree:
                new_grid[(x, y)] = (burning if any(grid.get((x + dx, y + dy), space) == burning for dx, dy in hood) or random.random() <= f else tree)
    return new_grid


# Main function. Initialises grid, then shows, updates, and
# waits for 1/60 of a second.
def main():
    grid = initialise()
    while True:
        show_grid(grid)
        grid = update_grid(grid)
        time.sleep(1 / 60.0)


# Catches control-c and exits cleanly
try:
    main()

except KeyboardInterrupt:
    print("Exiting")

# FIN!
