#!/usr/bin/env python3
import time
import sys

from colorsys import hsv_to_rgb

from PIL import Image, ImageDraw, ImageFont
from minicorn import Minicorn

# The text we want to display. You should probably keep this line and replace it below
# That way you'll have a guide as to what characters are supported!
text = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789 #@&!?{}<>[]();:.,'%*=+-=$_\\/ :-)"

minicorn = Minicorn()

rotation = 0
if len(sys.argv) > 1:
    try:
        rotation = int(sys.argv[1])
    except ValueError:
        print("Usage: {} <rotation>".format(sys.argv[0]))
        sys.exit(1)

minicorn.set_rotation(rotation)
display_width, display_height = minicorn.get_shape()

print("{}x{}".format(display_width, display_height))

# Do not look at minicorn with remaining eye
minicorn.set_brightness(0.1)

font = ImageFont.truetype("5x7.ttf", 8)

image = Image.open("twister.png")

offset_y = 0

while True:
    minicorn.set_image(image, offset_y=offset_y, wrap=True)

    offset_y += 1

    minicorn.show()
    time.sleep(0.01)
