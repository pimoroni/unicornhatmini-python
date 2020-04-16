#!/usr/bin/env python3

import time
from colorsys import hsv_to_rgb
from unicornhatmini import UnicornHATMini

print("""Unicorn HAT Mini: colour-cycle.py

Cycles through colour hues across all of Unicorn HAT Mini's pixels.

Press Ctrl+C to exit!

""")

unicornhatmini = UnicornHATMini()
unicornhatmini.set_brightness(0.1)

while True:
    hue = (time.time() / 10.0)
    r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1.0, 1.0)]
    unicornhatmini.set_all(r, g, b)
    unicornhatmini.show()
    time.sleep(1.0 / 60)
