import mock


def test_setup(GPIO, spidev):
    from unicornhatmini import UnicornHATMini
    unicornhatmini = UnicornHATMini()

    spidev.SpiDev.assert_has_calls((
        mock.call(0, 0),
        mock.call(0, 1)
    ), any_order=True)

    GPIO.setwarnings.assert_called_once_with(False)
    GPIO.setmode.assert_called_once_with(GPIO.BCM)

    del unicornhatmini


def test_shutdown(GPIO, spidev, atexit):
    from unicornhatmini import UnicornHATMini
    unicornhatmini = UnicornHATMini()

    atexit.register.assert_called_once_with(unicornhatmini._exit)
    unicornhatmini._exit()
