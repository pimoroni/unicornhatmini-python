import time

from colorsys import hsv_to_rgb

from minicorn import Minicorn, ROWS, COLS

minicorn = Minicorn()

minicorn.brightness(0.1)

while True:
    for y in range(ROWS):
        for x in range(COLS):
            hue = (time.time() / 10.0) + (x / float(COLS * 2))
            r, g, b = [int(c * 63.0) for c in hsv_to_rgb(hue, 1.0, 1.0)]
            minicorn.set_pixel(x, y, r, g, b)
    minicorn.show()
    time.sleep(1.0 / 60)
