"""
Generators: functions that produce values one at a time with `yield`.
Interview tip: generators are lazy - they use almost no memory, even for huge or infinite sequences.
"""
import sys
from itertools import islice


# A regular function builds the whole list in memory
def squares_list(n):
    result = []
    for i in range(n):
        result.append(i * i)
    return result


# A generator function yields one value at a time
def squares_gen(n):
    for i in range(n):
        yield i * i  # Pauses here and resumes on the next call to next()


print(squares_list(5))        # [0, 1, 4, 9, 16]
print(list(squares_gen(5)))   # [0, 1, 4, 9, 16]

# Memory comparison
print(sys.getsizeof(squares_list(100_000)))  # ~800,000 bytes
print(sys.getsizeof(squares_gen(100_000)))   # ~200 bytes

# Calling next() manually
gen = squares_gen(3)
print(next(gen))  # 0
print(next(gen))  # 1
print(next(gen))  # 4
try:
    next(gen)
except StopIteration:
    print("Generator is exhausted")  # A generator can only be used once!


# Infinite generator - fine because values are only made when asked for
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


first_10 = list(islice(fibonacci(), 10))  # Take only the first 10
print(first_10)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


# Pipelines: chain generators together, each line is processed one at a time
def read_lines(path):
    with open(path) as file:
        for line in file:  # Files are already lazy iterators
            yield line.strip()


def non_empty(lines):
    for line in lines:
        if line:
            yield line


for line in non_empty(read_lines("data/input.txt")):
    print(line)


# yield from: delegate to another iterable
def chain(*iterables):
    for iterable in iterables:
        yield from iterable


print(list(chain([1, 2], (3, 4), "ab")))  # [1, 2, 3, 4, 'a', 'b']
