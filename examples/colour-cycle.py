import time

from colorsys import hsv_to_rgb

from minicorn import Minicorn

minicorn = Minicorn()

minicorn.brightness(1.0)

while True:
    hue = (time.time() / 50.0)
    r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1.0, 1.0)]
    minicorn.set_all(r, g, b)
    minicorn.show()
    time.sleep(1.0 / 60)
