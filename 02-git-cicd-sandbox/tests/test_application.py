import pytest

from application import add, divide, exponent, multiply, subtract


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(10, 4) == 6


def test_multiply():
    assert multiply(6, 7) == 42


def test_divide():
    assert divide(7, 2) == 3.5


def test_divide_by_zero_raises():
    with pytest.raises(ValueError, match="cannot divide by zero"):
        divide(10, 0)


def test_exponent():
    assert exponent(2, 8) == 256
    assert exponent(5, 2) == 25
