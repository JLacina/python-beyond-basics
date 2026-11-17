"""
Context managers: the `with` statement guarantees setup and cleanup code runs.
Interview tip: know both ways to write one - a class with __enter__/__exit__,
or a generator with @contextmanager.
"""
import time
from contextlib import contextmanager, suppress


# You already use one: the file is closed even if an error happens inside the block
with open("data/input.txt") as file:
    first_line = file.readline()
print(file.closed)  # True


# Option 1: a class with __enter__ and __exit__
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self  # This is what `as` gets

    def __exit__(self, exc_type, exc_value, traceback):
        self.elapsed = time.perf_counter() - self.start
        print(f"Block took {self.elapsed:.4f}s")
        return False  # False = don't swallow exceptions (re-raise them)


with Timer() as t:
    sum(range(1_000_000))
print(f"Saved on the object too: {t.elapsed:.4f}s")


# Option 2: a generator with @contextmanager (shorter)
@contextmanager
def timer(label):
    start = time.perf_counter()
    try:
        yield  # Code inside the `with` block runs here
    finally:   # finally = runs even if the block raised an error
        print(f"{label} took {time.perf_counter() - start:.4f}s")


with timer("Sorting"):
    sorted(range(1_000_000, 0, -1))


# Cleanup runs even when there's an error
try:
    with timer("Failing block"):
        raise ValueError("Oops")
except ValueError:
    print("Error was still raised, but the timer printed first")


# Useful built-in: suppress specific exceptions
with suppress(FileNotFoundError):
    open("does_not_exist.txt")
print("Carried on without crashing")


# Multiple context managers in one with
with open("data/input.txt") as numbers_file, open("data/output.txt") as poem_file:
    print(numbers_file.readline().strip(), "|", poem_file.readline().strip())
