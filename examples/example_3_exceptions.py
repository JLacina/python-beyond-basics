"""
Exceptions: handle errors instead of letting the program crash.

Dividing by zero raises a ZeroDivisionError. Wrapping the risky code in try/except
lets us catch that specific error and carry on with a sensible fallback value.
See example_3b_advanced_exceptions.py for multiple exception types, else/finally
and custom exceptions.
"""
num = 0

try:
    inverse = 1 / num            # The risky line
except ZeroDivisionError:        # Only catch the error you expect - never a bare `except:`
    inverse = "not defined"

print(f"Inverse of {num} is {inverse}")
