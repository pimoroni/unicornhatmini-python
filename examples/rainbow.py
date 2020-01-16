#!/usr/bin/env python3

import time
import math
from colorsys import hsv_to_rgb
from minicorn import Minicorn

print("""Minicorn: rainbow.py

Displays a concentric rainbow that moves around the Minicorn display.

Press Ctrl+C to exit!

""")

minicorn = Minicorn()
minicorn.set_brightness(0.1)
minicorn.set_rotation(0)
width, height = minicorn.get_shape()

step = 0

while True:
    step += 1

    for x in range(0, width):
        for y in range(0, height):
            dx = (math.sin(step / width + 20) * width) + height
            dy = (math.cos(step / height) * height) + height
            sc = (math.cos(step / height) * height) + width

            hue = math.sqrt(math.pow(x - dx, 2) + math.pow(y - dy, 2)) / sc
            r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1, 1)]

            minicorn.set_pixel(x, y, r, g, b)

    minicorn.show()
    time.sleep(1.0 / 60)
