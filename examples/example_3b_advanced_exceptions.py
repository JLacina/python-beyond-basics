"""
Advanced exceptions: catching several types, else/finally, and custom exceptions.

Try running it with: 4 (works), 0 (ZeroDivisionError), abc (ValueError).
Note: the last line deliberately raises MyCustomError so you can see what a
custom exception looks like in a traceback - the script always ends with that error.
"""
num = input("Number: ")

try:
    inverse = 1 / int(num)
except (ZeroDivisionError, ValueError):
    inverse = "not defined"

print(f"Inverse of {num} is {inverse}")


try:
    inverse = 1 / int(num)
except ZeroDivisionError:  # Catch multiple error types with different behaviour
    inverse = "+/- infinity"
except ValueError:
    inverse = "not defined"
except Exception as e:
    print(repr(e))


try:
    int("5")
except ValueError:
    print("Fail!")
else:
    print("Everything worked")    # Runs after try block finishes without errors
finally:
    print("This always happens")  # Runs after everything, even if there was an error


# Custom exceptions: subclass Exception so callers can catch YOUR specific error
class MyCustomError(Exception):
    pass


raise MyCustomError("Here's an error message")
