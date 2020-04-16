#!/usr/bin/env python3

import time
import math
from colorsys import hsv_to_rgb
from unicornhatmini import UnicornHATMini

print("""Unicorn HAT Mini: rainbow.py

Displays a concentric rainbow that moves around the Unicorn HAT Mini display.

Press Ctrl+C to exit!

""")

unicornhatmini = UnicornHATMini()
unicornhatmini.set_brightness(0.1)
unicornhatmini.set_rotation(0)
width, height = unicornhatmini.get_shape()

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

            unicornhatmini.set_pixel(x, y, r, g, b)

    unicornhatmini.show()
    time.sleep(1.0 / 60)
