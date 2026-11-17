"""
Comprehensions: build lists, dicts and sets in one readable line.
Interview tip: use them for simple transforms/filters, use a regular loop when the logic gets complicated.
"""
from pprint import pprint

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# List comprehension: [expression for item in iterable]
squares = [n * n for n in numbers]
print(squares)  # [1, 4, 9, ..., 100]

# Same thing with a for loop
squares_loop = []
for n in numbers:
    squares_loop.append(n * n)
assert squares == squares_loop

# With a filter: [expression for item in iterable if condition]
even_squares = [n * n for n in numbers if n % 2 == 0]
print(even_squares)  # [4, 16, 36, 64, 100]

# With if/else (goes BEFORE the for)
labels = ["even" if n % 2 == 0 else "odd" for n in numbers]
print(labels)

# Dict comprehension: {key: value for item in iterable}
countries = ["Canada", "Mexico", "Brazil", "Chile"]
name_lengths = {country: len(country) for country in countries}
pprint(name_lengths)

# Swap keys and values
codes = {"CA": "Canada", "MX": "Mexico"}
names_to_codes = {name: code for code, name in codes.items()}
print(names_to_codes)  # {'Canada': 'CA', 'Mexico': 'MX'}

# Set comprehension: {expression for item in iterable} -> removes duplicates
first_letters = {country[0] for country in countries}
print(first_letters)  # {'C', 'M', 'B'} (order not guaranteed)

# Nested comprehension: flatten a list of lists
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [value for row in matrix for value in row]  # Read left to right like nested for loops
print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Transpose a matrix
transposed = [[row[i] for row in matrix] for i in range(3)]
print(transposed)  # [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

# Generator expression: round brackets, lazy (doesn't build a list in memory)
total = sum(n * n for n in range(1_000_000))
print(f"{total:,}")

# Useful built-ins that pair well with comprehensions
print(any(n > 9 for n in numbers))  # True if at least one is True
print(all(n > 0 for n in numbers))  # True if all are True
