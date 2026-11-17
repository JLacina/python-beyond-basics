"""
Write your own memoize decorator (without using functools.lru_cache)
and a decorator that counts how many times a function is called.
Practises: decorators, closures, *args, dicts
"""

# Todo: Write a `memoize` decorator that stores results in a dict keyed by the arguments

# Todo: Write a `count_calls` decorator that adds a `.calls` attribute to the function

# Todo: Use both on a recursive fibonacci function and check:
#  - fib(30) == 832040
#  - fib.calls is much smaller with @memoize than without
