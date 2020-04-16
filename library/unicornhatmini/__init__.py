#!/usr/bin/env python3

import time
import atexit

import spidev

from colorsys import hsv_to_rgb

import RPi.GPIO as GPIO

__version__ = '0.0.1'


# Holtek HT16D35
CMD_SOFT_RESET = 0xCC
CMD_GLOBAL_BRIGHTNESS = 0x37
CMD_COM_PIN_CTRL = 0x41
CMD_ROW_PIN_CTRL = 0x42
CMD_WRITE_DISPLAY = 0x80
CMD_READ_DISPLAY = 0x81
CMD_SYSTEM_CTRL = 0x35
CMD_SCROLL_CTRL = 0x20

_COLS = 17
_ROWS = 7

BUTTON_A = 5
BUTTON_B = 6
BUTTON_X = 16
BUTTON_Y = 20


class UnicornHATMini():
    lut = [[139, 138, 137], [223, 222, 221], [167, 166, 165], [195, 194, 193], [111, 110, 109], [55, 54, 53], [83, 82, 81], [136, 135, 134], [220, 219, 218], [164, 163, 162], [192, 191, 190], [108, 107, 106], [52, 51, 50], [80, 79, 78], [113, 115, 114], [197, 199, 198], [141, 143, 142], [169, 171, 170], [85, 87, 86], [29, 31, 30], [57, 59, 58], [116, 118, 117], [200, 202, 201], [144, 146, 145], [172, 174, 173], [88, 90, 89], [32, 34, 33], [60, 62, 61], [119, 121, 120], [203, 205, 204], [147, 149, 148], [175, 177, 176], [91, 93, 92], [35, 37, 36], [63, 65, 64], [122, 124, 123], [206, 208, 207], [150, 152, 151], [178, 180, 179], [94, 96, 95], [38, 40, 39], [66, 68, 67], [125, 127, 126], [209, 211, 210], [153, 155, 154], [181, 183, 182], [97, 99, 98], [41, 43, 42], [69, 71, 70], [128, 130, 129], [212, 214, 213], [156, 158, 157], [184, 186, 185], [100, 102, 101], [44, 46, 45], [72, 74, 73], [131, 133, 132], [215, 217, 216], [159, 161, 160], [187, 189, 188], [103, 105, 104], [47, 49, 48], [75, 77, 76], [363, 362, 361], [447, 446, 445], [391, 390, 389], [419, 418, 417], [335, 334, 333], [279, 278, 277], [307, 306, 305], [360, 359, 358], [444, 443, 442], [388, 387, 386], [416, 415, 414], [332, 331, 330], [276, 275, 274], [304, 303, 302], [337, 339, 338], [421, 423, 422], [365, 367, 366], [393, 395, 394], [309, 311, 310], [253, 255, 254], [281, 283, 282], [340, 342, 341], [424, 426, 425], [368, 370, 369], [396, 398, 397], [312, 314, 313], [256, 258, 257], [284, 286, 285], [343, 345, 344], [427, 429, 428], [371, 373, 372], [399, 401, 400], [315, 317, 316], [259, 261, 260], [287, 289, 288], [346, 348, 347], [430, 432, 431], [374, 376, 375], [402, 404, 403], [318, 320, 319], [262, 264, 263], [290, 292, 291], [349, 351, 350], [433, 435, 434], [377, 379, 378], [405, 407, 406], [321, 323, 322], [265, 267, 266], [293, 295, 294], [352, 354, 353], [436, 438, 437], [380, 382, 381], [408, 410, 409], [324, 326, 325], [268, 270, 269], [296, 298, 297]]

    def __init__(self, spi_max_speed_hz=600000):
        """Initialise unicornhatmini

        Tested to around 6MHz (500fps) on a Pi 4 and 6KHz (50fps) on an A+.

        :param spi_max_speed_hz: SPI speed in Hz
        """
        self.disp = [[0, 0, 0] for _ in range(_COLS * _ROWS)]
        self.left_matrix = (spidev.SpiDev(0, 0), 8, 0)
        self.right_matrix = (spidev.SpiDev(0, 1), 7, 28 * 8)

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        self.buf = [0 for _ in range(28 * 8 * 2)]
        self._rotation = 0

        for device, pin, offset in self.left_matrix, self.right_matrix:
            device.no_cs = True
            device.cshigh = False
            device.max_speed_hz = spi_max_speed_hz
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
            self.xfer(device, pin, [CMD_SOFT_RESET])
            self.xfer(device, pin, [CMD_GLOBAL_BRIGHTNESS, 0x01])
            self.xfer(device, pin, [CMD_SCROLL_CTRL, 0x00])
            self.xfer(device, pin, [CMD_SYSTEM_CTRL, 0x00])
            self.xfer(device, pin, [CMD_WRITE_DISPLAY, 0x00] + self.buf[offset:offset + (28 * 8)])
            self.xfer(device, pin, [CMD_COM_PIN_CTRL, 0xff])
            self.xfer(device, pin, [CMD_ROW_PIN_CTRL, 0xff, 0xff, 0xff, 0xff])
            self.xfer(device, pin, [CMD_SYSTEM_CTRL, 0x03])

        atexit.register(self._exit)

    def _shutdown(self):
        for device, pin, _ in self.left_matrix, self.right_matrix:
            self.xfer(device, pin, [CMD_COM_PIN_CTRL, 0x00])
            self.xfer(device, pin, [CMD_ROW_PIN_CTRL, 0x00, 0x00, 0x00, 0x00])
            self.xfer(device, pin, [CMD_SYSTEM_CTRL, 0x00])

    def _exit(self):
        self._shutdown()

    def xfer(self, device, pin, command):
        GPIO.output(pin, GPIO.LOW)
        device.xfer2(command)
        GPIO.output(pin, GPIO.HIGH)

    def set_pixel(self, x, y, r, g, b):
        """Set a single pixel."""
        offset = (x * _ROWS) + y
        if self._rotation == 90:
            y = _COLS - 1 - y
            offset = (y * _ROWS) + x
        if self._rotation == 180:
            x = _COLS - 1 - x
            y = _ROWS - 1 - y
            offset = (x * _ROWS) + y
        if self._rotation == 270:
            x = _ROWS - 1 - x
            offset = (y * _ROWS) + x
        self.disp[offset] = [r >> 2, g >> 2, b >> 2]

    def set_all(self, r, g, b):
        """Set all pixels."""
        r >>= 2
        g >>= 2
        b >>= 2
        for i in range(_ROWS * _COLS):
            self.disp[i] = [r, g, b]

    def set_image(self, image, offset_x=0, offset_y=0, wrap=False, bg_color=(0, 0, 0)):
        """Set a PIL image to the display buffer."""
        image_width, image_height = image.size

        if image.mode != "RGB":
            image = image.convert('RGB')

        display_width, display_height = self.get_shape()

        for y in range(display_height):
            for x in range(display_width):
                r, g, b = bg_color
                i_x = x + offset_x
                i_y = y + offset_y
                if wrap:
                    while i_x >= image_width:
                        i_x -= image_width
                    while i_y >= image_height:
                        i_y -= image_height
                if i_x < image_width and i_y < image_height:
                    r, g, b = image.getpixel((i_x, i_y))
                self.set_pixel(x, y, r, g, b)

    def clear(self):
        """Set all pixels to 0."""
        self.set_all(0, 0, 0)

    def set_brightness(self, b=0.2):
        for device, pin, _ in self.left_matrix, self.right_matrix:
            self.xfer(device, pin, [CMD_GLOBAL_BRIGHTNESS, int(63 * b)])

    def set_rotation(self, rotation=0):
        if rotation not in [0, 90, 180, 270]:
            raise ValueError("Rotation must be one of 0, 90, 180, 270")
        self._rotation = rotation

    def show(self):
        for i in range(_COLS * _ROWS):
            ir, ig, ib = self.lut[i]
            r, g, b = self.disp[i]
            self.buf[ir] = r
            self.buf[ig] = g
            self.buf[ib] = b

        for device, pin, offset in self.left_matrix, self.right_matrix:
            self.xfer(device, pin, [CMD_WRITE_DISPLAY, 0x00] + self.buf[offset:offset + (28 * 8)])

    def get_shape(self):
        if self._rotation in [90, 270]:
            return _ROWS, _COLS
        else:
            return _COLS, _ROWS


if __name__ == "__main__":
    unicornhatmini = UnicornHATMini()

    while True:
        for y in range(_ROWS):
            for x in range(_COLS):
                hue = (time.time() / 4.0) + (x / float(_COLS * 2)) + (y / float(_ROWS))
                r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1.0, 1.0)]
                unicornhatmini.set_pixel(x, y, r, g, b)
        unicornhatmini.show()
        time.sleep(1.0 / 60)
