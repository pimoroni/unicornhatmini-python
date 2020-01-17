#!/usr/bin/env python3
import time
import random

from gpiozero import Button
from minicorn import Minicorn

minicorn = Minicorn()
minicorn.set_rotation(270)


class Game:
    def __init__(self, display):
        self.display = display
        self.playing_field = [[(0, 0, 0) for x in range(7)] for y in range(17)]
        self.current = None
        self.drop_speed = 3  # Pixels per second

    def new_column(self):
        if self.current is None:
           self.current = Column(3, -3)

    def update(self, fps=50.0):
        t = time.time()
        self.new_column()
        self.drop(float(self.drop_speed) / fps)
        self.collide()

        self.display.clear()
        for x in range(7):
            for y in range(17):
                self.display.set_pixel(x, y, *self.playing_field[y][x])

        if self.current is not None:
            self.current.draw(self.display)

        self.display.show()

    def collide(self):
        if self.current is not None:
            bottom_y = int(self.current.y) + 3
            if bottom_y >= 17:
                self.current.bake(self.playing_field)
                self.current = None
                return
            if self.playing_field[bottom_y][self.current.x] != (0, 0, 0):
                self.current.bake(self.playing_field)
                self.current = None
                return

    def drop(self, distance=1.0):
        if self.current is not None:
            self.current.drop(distance)

    def move(self):
        if self.current is not None:
            self.current.move()

    def rotate(self):
        if self.current is not None:
            self.current.rotate()


class Column:
    def __init__(self, x, y):
        self.colors = [
            (255, 30, 30),
            (30, 255, 30),
            (30, 30, 255)
        ]
        self.x = x
        self.y = y
        self.sequence = [
            random.choice(self.colors),    
            random.choice(self.colors),    
            random.choice(self.colors),    
        ]

    def rotate(self):
        self.sequence.insert(0, self.sequence.pop(2))

    def move(self):
        self.x += 1
        self.x %= 7

    def drop(self, distance):
        self.y += distance

    def draw(self, display):
        for i, color in enumerate(self.sequence):
            if int(self.y) + i >= 0:
                display.set_pixel(self.x, int(self.y) + i, *color)

    def bake(self, field):
        for i, color in enumerate(self.sequence):
            field[int(self.y) + i][self.x] = color


button_a = Button(5)   # Red
button_b = Button(6)   # [B]lue
button_x = Button(16)  # Green
button_y = Button(20)  # [Y]ellow

game = Game(minicorn)

button_y.when_pressed = game.rotate
button_x.when_pressed = game.move

while True:
    game.update()
    time.sleep(1.0 / 50.0)
