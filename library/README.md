# Unicorn HAT Mini

[![Build Status](https://travis-ci.com/pimoroni/unicornhatmini-python.svg?branch=master)](https://travis-ci.com/pimoroni/unicornhatmini-python)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/unicornhatmini-python/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/unicornhatmini-python?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/unicornhatmini.svg)](https://pypi.python.org/pypi/unicornhatmini)
[![Python Versions](https://img.shields.io/pypi/pyversions/unicornhatmini.svg)](https://pypi.python.org/pypi/unicornhatmini)

# Requirements

You must enable SPI on your Raspberry Pi:

* Run: `sudo raspi-config nonint do_spi 0`

# Installing

Stable library from PyPi:

* Just run `sudo pip3 install unicornhatmini`

Or for Python 2:

* `sudo pip install unicornhatmini`

Latest/development library from GitHub:

* `git clone https://github.com/pimoroni/unicornhatmini-python`
* `cd unicornhatmini-python`
* `sudo ./install.sh`


# Changelog
0.0.2
-----

* Fix for Pi kernel 5.4.51, removed cshigh setting from SPI setup

0.0.1
-----

* Initial Release
