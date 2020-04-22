#!/usr/bin/env python3
import time
import sys


from PIL import Image
from unicornhatmini import UnicornHATMini


unicornhatmini = UnicornHATMini()

rotation = 0

if len(sys.argv) > 1:
    try:
        rotation = int(sys.argv[1])
    except ValueError:
        print("Usage: {} <rotation>".format(sys.argv[0]))
        sys.exit(1)

unicornhatmini.set_rotation(rotation)
display_width, display_height = unicornhatmini.get_shape()

print("{}x{}".format(display_width, display_height))

# Do not look at unicornhatmini with remaining eye
unicornhatmini.set_brightness(0.1)

image = Image.open("twister.png")

offset_y = 0

while True:
    unicornhatmini.set_image(image, offset_y=offset_y, wrap=True)

    offset_y += 1

    unicornhatmini.show()
    time.sleep(0.01)
