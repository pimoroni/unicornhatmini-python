import sys
import pytest
import mock


@pytest.fixture(scope='function', autouse=True)
def cleanup():
    """This fixture removes modules under test from sys.modules.

    This ensures that each module is fully re-imported, along with
    the fixtures for each test function.

    """

    yield None
    del sys.modules["unicornhatmini"]


@pytest.fixture(scope='function', autouse=False)
def spidev():
    """Mock spidev module."""

    spidev = mock.MagicMock()
    sys.modules['spidev'] = spidev
    yield spidev
    del sys.modules['spidev']


@pytest.fixture(scope='function', autouse=False)
def GPIO():
    """Mock RPi.GPIO module."""
    GPIO = mock.MagicMock()
    # Fudge for Python < 37 (possibly earlier)
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi'].GPIO = GPIO
    sys.modules['RPi.GPIO'] = GPIO
    yield GPIO
    del sys.modules['RPi']
    del sys.modules['RPi.GPIO']


@pytest.fixture(scope='function', autouse=False)
def atexit():
    """Mock atexit module."""

    atexit = mock.MagicMock()
    sys.modules['atexit'] = atexit
    yield atexit
    del sys.modules['atexit']
