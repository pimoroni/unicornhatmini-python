#!/usr/bin/env python3
import time
import random

from gpiozero import Button
from unicornhatmini import UnicornHATMini

unicornhatmini = UnicornHATMini()
unicornhatmini.set_rotation(270)


class Game:
    def __init__(self, display):
        self.display = display
        self.playing_field = [[(0, 0, 0) for x in range(7)] for y in range(17)]
        self.remove = [[0 for x in range(7)] for y in range(17)]
        self.current = None
        self.drop_speed = 6  # Pixels per second
        self._move = False
        self._rotate = False
        self.new_column()

    def new_column(self):
        self.current = Column(3, -3)

    def update(self, fps=50.0):
        if self._move:
            self.current.move(self.playing_field, 1.0, 0)
            self._move = False

        if self._rotate:
            self.current.rotate()
            self._rotate = False

        if self.current.move(self.playing_field, 0, float(self.drop_speed) / fps):
            self.current.bake(self.playing_field)
            self.new_column()

        self.update_field()
        self.remove_blocks()

        self.display.clear()
        for x in range(7):
            for y in range(17):
                self.display.set_pixel(x, y, *self.playing_field[y][x])

        self.current.draw(self.display)

        self.display.show()

    def get_chain(self, chain, x, y, direction, previous_block):
        nx, ny = direction
        if x + nx < 7 and y + ny < 17 and x + nx >= 0 and y + ny >= 0:
            skip = self.remove[y + ny][x + nx]
            block = self.playing_field[y + ny][x + nx]
            if skip or block != previous_block:
                # Block already scheduled for deletion
                return chain

            # Add block to the current chain
            chain += [(x + nx, y + ny)]
            chain = self.get_chain(chain, x + nx, y + ny, direction, block)

        return chain

    def update_field(self):
        directions = [
            (0, -1), (1, -1),
                     (1, 0),
                     (1, 1)
        ]

        remove = []

        for y in range(17):
            for x in range(7):
                skip = self.remove[y][x]
                block = self.playing_field[y][x]
                if skip or block == (0, 0, 0):
                    # Block is scheduled for deletion
                    continue

                for d in directions:
                    chain = [(x, y)]
                    chain = self.get_chain(chain, x, y, d, block)
                    if len(chain) >= 3:
                        remove += chain

        for x, y in remove:
            self.remove[y][x] = 1
            self.playing_field[y][x] = (128, 128, 128)

    def remove_blocks(self):
        for y in range(17):
            for x in range(7):
                remove = self.remove[y][x]
                block = self.playing_field[y][x]

                if remove:
                    new_block = [max(0, int(c * 0.8)) for c in block]
                    new_block = [0 if c < 5 else c for c in new_block]
                    self.playing_field[y][x] = tuple(new_block)
                    if tuple(new_block) == (0, 0, 0):
                        self.remove[y][x] = 0  # Removal done
                        drop = y
                        while drop > 0:
                            self.playing_field[drop][x] = self.playing_field[drop - 1][x]
                            drop -= 1

    def move(self):
        self._move = True

    def rotate(self):
        self._rotate = True


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

    def move(self, field, x=0, y=0):
        field_h = len(field)
        field_w = len(field[0])

        if x > 0:
            new_x = int(self.x + x) % 7
            collissions = [col[new_x] for col in field[int(self.y):int(self.y) + 3]]
            for block in collissions:
                if block != (0, 0, 0):
                    return True

            self.x = new_x

        if y > 0:
            new_y = self.y + y

            if int(new_y + 2) >= field_h:
                return True

            if field[int(new_y) + 2][self.x] != (0, 0, 0):
                return True

            self.y = new_y

        return False

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
button_y = Button(24)  # [Y]ellow

game = Game(unicornhatmini)

button_y.when_pressed = game.rotate
button_x.when_pressed = game.move

while True:
    game.update()
    time.sleep(1.0 / 50.0)
