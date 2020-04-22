# Reference <!-- omit in toc -->

- [Getting Started](#getting-started)
  - [Installing](#installing)
  - [Examples](#examples)
    - [Buttons](#buttons)
    - [Colour Cycle](#colour-cycle)
    - [Columns](#columns)
    - [Demo](#demo)
    - [Forest Fire](#forest-fire)
    - [FPS](#fps)
    - [Image](#image)
    - [Rainbow](#rainbow)
    - [Simon](#simon)
- [Function Reference](#function-reference)
  - [Setting Pixels](#setting-pixels)
  - [Setting An Image](#setting-an-image)
  - [Changing Global Brightness](#changing-global-brightness)
  - [Clearing The Display](#clearing-the-display)
  - [Displaying The Result](#displaying-the-result)
  - [Using The Buttons](#using-the-buttons)

## Getting Started

Unicorn HAT Mini includes an array of 17x7 LEDs you can control by setting individual pixels, or whole pre-prepared images.

It also includes four buttons on BCM pins 5, 6, 16 and 24. We demonstrate using the GPIO Zero library with these.

### Installing

Most people should grab the library from GitHub and run our simple installer:

```
git clone https://github.com/pimoroni/unicornhatmini-python
cd unicornhatmini-python
sudo ./install.sh
```

This will ensure any dependencies are installed and copy examples into `~/Pimoroni/unicornhatmini/`

You can install just the Unicorn HAT Mini library by running:

```
sudo pip3 install unicornhatmini
```

## Examples

### Buttons
[buttons.py](examples/buttons.py)

Demonstrates the use of Unicorn HAT Mini's buttons with the GPIO Zero library.

### Colour Cycle
[colour-cycle.py](examples/colour-cycle.py)

Cycles through colour hues across all of Unicorn HAT Mini's pixels.

### Columns
[columns.py](examples/columns.py)

Stack columns of coloured lights in this simple game.

Button Y will rotate the order of the coloured lights in a column.

Button X will move the column to the right, wrapping around to the left of the screen if it crosses the right edge.

### Demo
[demo.py](examples/demo.py)

Displays a sequence of 4 demoscene style effects across Unicorn HAT mini.

1. Tunnel effect
2. Rainbow Searchlights effect
3. Checkerboard effect
4. Swirl effect

### Forest Fire
[forest-fire.py](examples/forest-fire.py)

A classic cellular automata simulating the growth of forest (green lights) and outbreak of fires (red lights).

### FPS
[fps.py](examples/fps.py)

Will try to refresh the Unicorn HAT Mini display as fast as possible and display the framerate in the terminal.

You can change the update rate, and consequently the framerate, by changing the `spi_max_speed_hz` parameter when constructing a new `UnicornHATMini()` instance.


### Image
[image.py](examples/image.py)

Demonstrates the use of PIL (Python Image Library) to create an image and display it upon Unicorn HAT Mini.

In this case it's scrolling an image longer than the display to produce a wavy line pattern.

Whether you're scrolling text or displaying a UI for your project, you'll probably use PIL.

### Rainbow
[rainbow.py](examples/rainbow.py)

Displays a concentric rainbow that moves around the Unicorn HAT Mini display.

### Simon
[simon.py](examples/simon.py)

A simple game. Repeat the colour sequence at each step to proceed and see how long a sequence you can memorise. Colours will flash up adjacent to their corresponding buttons.

## Function Reference

In all cases you'll need to first initialise the Unicorn HAT Mini library like so:

```python
from unicornhatmini import UnicornHATMini

unicornhatmini = UnicornHATMini()
```

`UnicornHATMini` takes one argument, `spi_max_speed_hz` which you can use to allow faster SPI speeds and achieve better framerates. In most cases, however, how much you try to draw will have a bigger impact.

### Setting Pixels

You can set either one or all pixels with `set_pixel` or `set_all` respectively.

#### set_pixel

`set_pixel` requires an `x` and `y` value starting from `0,0` and ending at `16,6` (zero indexed, 17 by 7 pixel display). For example at normal rotation the top left corner would be `0,0` and the bottom right `16,6`. A handy mnemonic for remembering which is left/right and which is up/down is "Along the corridor and down the stairs."

If you rotate Unicorn HAT Mini by `90` or `270` degrees then it becomes 7 by 17 pixels in size, so your coordinates must change accordingly.

`set_pixel` also requires three colour values, one for red, one for green and one for blue.

For example `unicornhatmini.set_pixel(0, 0, 255, 0, 0)` would set the top left pixel to red.

#### set_all

`set_all` is very similar to `set_pixel` except it does not require an `x` and `y` coordinate, since the colour you're setting applies to all pixels.

For example `unicornhatmini.set_all(0, 255, 0)` would set all pixels to green.

### Setting An Image

For any complex drawing - such as text, images and icons - you will want to use the Python Image Library to create an image, and `set_image` to copy it to Unicorn HAT Mini.

`set_image` accepts a PIL image of any size, so you can display part of a larger image to achieve scrolling affects.

To set a blank red PIL image to Unicorn HAT Mini you might:

```python
from PIL import Image

from unicornhatmini import UnicornHATMini
unicornhatmini = UnicornHATMini()

image = Image.new("RGB", (17, 7), (255, 0, 0))

unicornhatmini.set_image(image)
unicornhatmini.show()
```

If you've drawn an image you want to display and saved it to a file, you could do something like:

```python
from PIL import Image

from unicornhatmini import UnicornHATMini
unicornhatmini = UnicornHATMini()

image = Image.open("my-image.png")

unicornhatmini.set_image(image)
unicornhatmini.show()
```

### Changing Global Brightness

Unicorn HAT Mini has a global brightness setting which you can change with `unicornhatmini.set_brightness`.

It accepts a value from `0.0` to `1.0` so for half brightness you would use:

```python
unicornhatmini.set_brightness(0.5)
```

### Clearing The Display

You can clear Unicorn HAT Mini to black using `unicornhatmini.clear()`. This is just an alias for `unicornhatmini.set_all(0, 0, 0)` which does the same thing.

### Displaying The Result

To send your image or carefully curated pixels to Unicorn HAT Mini you should call `unicornhatmini.show()`. This transfers the local buffer over to the display, and you'll usually want to call this once per frame after all of your drawing operations.

### Using The Buttons

To use the buttons on your Unicorn HAT Mini you should use the GPIO Zero library.

Unicorn HAT Mini has four buttons on pins BCM 5, 6, 16 and 24.

The example below shows how you might bind them to a function:

```python
from gpiozero import Button

def pressed(pin):
    print(f"Button on pin {pin} pressed!")

button_a = Button(5)
button_b = Button(6)
button_x = Button(16)
button_y = Button(24)

button_a.when_pressed = pressed
button_b.when_pressed = pressed
button_x.when_pressed = pressed
button_y.when_pressed = pressed
```
