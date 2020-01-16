#!/usr/bin/env python3

import time
import math
from colorsys import hsv_to_rgb
from minicorn import Minicorn, ROWS, COLS

print("""Minicorn: rainbow.py

Displays a concentric rainbow that moves around the Minicorn display.

Press Ctrl+C to exit!

""")

minicorn = Minicorn()
minicorn.brightness(0.1)

step = 0

while True:
    step += 1

    for x in range(0, COLS):
        for y in range(0, ROWS):
            dx = (math.sin(step / COLS + 20) * COLS) + ROWS
            dy = (math.cos(step / ROWS) * ROWS) + ROWS
            sc = (math.cos(step / ROWS) * ROWS) + COLS

            hue = math.sqrt(math.pow(x - dx, 2) + math.pow(y - dy, 2)) / sc
            r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1, 1)]

            minicorn.set_pixel(x, y, r, g, b)

    minicorn.show()
    time.sleep(1.0 / 60)
