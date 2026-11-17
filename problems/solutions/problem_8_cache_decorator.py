"""
Write your own memoize decorator (without using functools.lru_cache)
and a decorator that counts how many times a function is called.
"""
from functools import wraps


def memoize(func):
    cache = {}  # Lives in the closure, so it persists between calls

    @wraps(func)
    def wrapper(*args):
        if args not in cache:  # args is a tuple, so it can be a dict key
            cache[args] = func(*args)
        return cache[args]
    return wrapper


def count_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1  # Functions are objects, so they can have attributes
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


@count_calls
def slow_fib(n):
    if n < 2:
        return n
    return slow_fib(n - 1) + slow_fib(n - 2)


@memoize
@count_calls  # Count the real calls, not the cache hits
def fast_fib(n):
    if n < 2:
        return n
    return fast_fib(n - 1) + fast_fib(n - 2)


assert slow_fib(30) == 832040
assert fast_fib(30) == 832040

print(f"Without memoize: {slow_fib.calls:,} calls")             # 2,692,537
print(f"With memoize:    {fast_fib.__wrapped__.calls:,} calls")  # 31
