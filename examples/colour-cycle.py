#!/usr/bin/env python3

import time
from colorsys import hsv_to_rgb
from minicorn import Minicorn

print("""Minicorn: colour-cycle.py

Cycles through colour hues across all of Minicorn's pixels.

Press Ctrl+C to exit!

""")

minicorn = Minicorn()
minicorn.brightness(0.1)

while True:
    hue = (time.time() / 10.0)
    r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1.0, 1.0)]
    minicorn.set_all(r, g, b)
    minicorn.show()
    time.sleep(1.0 / 60)
