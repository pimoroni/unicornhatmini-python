"""Feature regression tests.

These tests aren't particularly rigorous,
but serve to guard against future regressions.

"""

import pytest
import mock


def test_set_pixel(GPIO, spidev):
    from unicornhatmini import UnicornHATMini
    unicornhatmini = UnicornHATMini()

    unicornhatmini.set_pixel(0, 0, 255, 255, 255)


def test_set_all(GPIO, spidev):
    from unicornhatmini import UnicornHATMini
    unicornhatmini = UnicornHATMini()

    unicornhatmini.set_all(255, 255, 255)

    assert unicornhatmini.disp == [[255 >> 2, 255 >> 2, 255 >> 2]] * (17 * 7)


def test_set_brightness(GPIO, spidev):
    from unicornhatmini import UnicornHATMini
    unicornhatmini = UnicornHATMini()

    unicornhatmini.set_brightness(0.5)


def test_show(GPIO, spidev):
    from unicornhatmini import UnicornHATMini
    unicornhatmini = UnicornHATMini()

    unicornhatmini.show()


def test_clear(GPIO, spidev):
    from unicornhatmini import UnicornHATMini
    unicornhatmini = UnicornHATMini()

    unicornhatmini.clear()

    assert unicornhatmini.disp == [[0, 0, 0]] * (17 * 7)


def test_set_rotation(GPIO, spidev):
    from unicornhatmini import UnicornHATMini
    unicornhatmini = UnicornHATMini()

    shapes = {
        0: (17, 7),
        90: (7, 17),
        180: (17, 7),
        270: (7, 17)
    }

    for rotation in (0, 90, 180, 270):
        unicornhatmini.set_rotation(rotation)
        assert unicornhatmini.get_shape() == shapes[rotation]
        unicornhatmini.set_pixel(0, 0, 255, 255, 255)


def test_set_rotation_invalid(GPIO, spidev):
    from unicornhatmini import UnicornHATMini
    unicornhatmini = UnicornHATMini()

    with pytest.raises(ValueError):
        unicornhatmini.set_rotation(99)


def test_set_image(GPIO, spidev):
    from unicornhatmini import UnicornHATMini
    unicornhatmini = UnicornHATMini()

    image = mock.MagicMock()
    image.size = (17, 7)
    image.getpixel.return_value = (255, 255, 255)
    image.convert.return_value = image
    unicornhatmini.set_image(image, offset_x=0, offset_y=0)

    image.mode = "RGB"
    unicornhatmini.set_image(image, offset_x=0, offset_y=0)


def test_set_image_wrap(GPIO, spidev):
    from unicornhatmini import UnicornHATMini
    unicornhatmini = UnicornHATMini()

    image = mock.MagicMock()
    image.size = (3, 3)
    image.mode = "RGB"
    image.getpixel.return_value = (255, 255, 255)
    unicornhatmini.set_image(image, offset_x=0, offset_y=0, wrap=True)
