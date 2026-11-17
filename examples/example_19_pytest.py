"""
Testing with pytest.
Run from the examples folder with:  python -m pytest example_19_pytest.py -v
(Install first with:  pip install pytest)

Interview tip: pytest finds functions named test_* and uses plain `assert`.
Know fixtures, parametrize, and how to test that an error is raised.
"""
import pytest


# Code under test (normally this would live in its own module)
def is_palindrome(text):
    cleaned = "".join(char.lower() for char in text if char.isalnum())
    return cleaned == cleaned[::-1]


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add(self, name, price):
        self.items[name] = price

    def total(self):
        return sum(self.items.values())


# A basic test: just assert
def test_palindrome_simple():
    assert is_palindrome("racecar")
    assert not is_palindrome("python")


# parametrize: run the same test with many inputs
@pytest.mark.parametrize("text, expected", [
    ("racecar", True),
    ("A man, a plan, a canal: Panama", True),
    ("", True),
    ("ab", False),
])
def test_palindrome_cases(text, expected):
    assert is_palindrome(text) == expected


# Testing that an exception is raised
def test_divide_by_zero():
    with pytest.raises(ValueError, match="divide by zero"):
        divide(1, 0)


# Comparing floats
def test_divide_float():
    assert divide(1, 3) == pytest.approx(0.3333, abs=1e-4)


# Fixtures: reusable setup, passed in by argument name
@pytest.fixture
def cart():
    cart = ShoppingCart()
    cart.add("apple", 1.50)
    cart.add("bread", 3.00)
    return cart


def test_cart_total(cart):
    assert cart.total() == 4.50


def test_cart_add(cart):
    cart.add("milk", 2.00)
    assert cart.total() == 6.50  # Each test gets a fresh fixture


# Built-in fixture: tmp_path gives you a temporary folder
def test_write_file(tmp_path):
    path = tmp_path / "hello.txt"
    path.write_text("hi")
    assert path.read_text() == "hi"
