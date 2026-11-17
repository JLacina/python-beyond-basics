"""
Decorators: functions that wrap other functions to add behaviour.
Interview tip: be able to write a decorator from scratch, explain functools.wraps,
and write one that takes arguments.
"""
import time
from functools import wraps, lru_cache


# Functions are objects: they can be passed around and returned
def shout(text):
    return text.upper()


def apply(func, value):
    return func(value)


print(apply(shout, "hello"))  # HELLO


# A basic decorator
def timer(func):
    @wraps(func)  # Keeps the original function's __name__ and docstring
    def wrapper(*args, **kwargs):  # Accept any arguments and pass them through
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result  # Don't forget to return the result!
    return wrapper


@timer  # Same as: slow_sum = timer(slow_sum)
def slow_sum(n):
    """Add up the numbers from 0 to n-1"""
    return sum(range(n))


print(slow_sum(1_000_000))
print(slow_sum.__name__, "-", slow_sum.__doc__)  # Without @wraps this would say "wrapper"


# A decorator that takes arguments: needs one extra layer
def retry(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
            raise RuntimeError(f"{func.__name__} failed after {times} attempts")
        return wrapper
    return decorator


calls = 0


@retry(times=3)
def flaky():
    global calls
    calls += 1
    if calls < 3:
        raise ConnectionError("Network glitch")
    return "Success!"


print(flaky())


# Built-in decorator: lru_cache memoizes results (great for recursion)
@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


print(fib(100))  # Instant - without the cache this would take forever
print(fib.cache_info())


# Stacking decorators: applied bottom to top
@timer
@lru_cache
def square(n):
    return n * n


square(4)
