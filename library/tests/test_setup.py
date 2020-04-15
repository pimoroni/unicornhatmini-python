import mock


def test_setup(GPIO, spidev):
    from minicorn import Minicorn
    minicorn = Minicorn()

    spidev.SpiDev.assert_has_calls((
        mock.call(0, 0),
        mock.call(0, 1)
    ), any_order=True)

    GPIO.setwarnings.assert_called_once_with(False)
    GPIO.setmode.assert_called_once_with(GPIO.BCM)

    del minicorn


def test_shutdown(GPIO, spidev, atexit):
    from minicorn import Minicorn
    minicorn = Minicorn()

    atexit.register.assert_called_once_with(minicorn._exit)
    minicorn._exit()
