#!/usr/bin/env python3

import time
from gpiozero import Button
from signal import pause
from unicornhatmini import UnicornHATMini

print("""Unicorn HAT Mini: target.py

Demonstrates the use of Unicorn HAT Mini's buttons to control c>

Press Ctrl+C to exit!

""")

uh = UnicornHATMini()
x = 0
y = 0

def display():
    uh.clear()
    for i in range(17):
        for j in range(7):
            if (i == x) or (j == y):
                if (i == x) and (j == y):
                    uh.set_pixel(i, j, 255, 0, 0)
                else:
                    uh.set_pixel(i, j, 0, 255, 0)
    uh.show()

def up():
    global y
    if y == 0:
        y = 6
    else:
        y = y - 1

def down():
    global y
    if y == 6:
        y = 0
    else:
        y = y + 1

def left():
    global x
    if x == 0:
        x = 16
    else:
        x = x - 1

def right():
    global x
    if x == 16:
        x = 0
    else:
        x = x + 1

def pressed(button):
    button_name = button_map[button.pin.number]
    if button == button_a:
        up()
    if button == button_b:
        down()
    if button == button_x:
        left()
    if button == button_y:
        right()
    display()

button_map = {5: "A",
              6: "B",
              16: "X",
              24: "Y"}

button_a = Button(5)
button_b = Button(6)
button_x = Button(16)
button_y = Button(24)

display()

try:
    button_a.when_pressed = pressed
    button_b.when_pressed = pressed
    button_x.when_pressed = pressed
    button_y.when_pressed = pressed

    pause()

except KeyboardInterrupt:
    button_a.close()
    button_b.close()
    button_x.close()
    button_y.close()
