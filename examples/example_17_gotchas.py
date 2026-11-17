"""
Common Python gotchas - these come up a lot in interviews!
"""
import copy


# 1. Mutable default arguments: the default is created ONCE, when the function is defined
def add_item_bad(item, items=[]):
    items.append(item)
    return items


print(add_item_bad("a"))  # ['a']
print(add_item_bad("b"))  # ['a', 'b']  <- surprise! Same list is reused


def add_item_good(item, items=None):
    if items is None:
        items = []  # A new list on every call
    items.append(item)
    return items


print(add_item_good("a"))  # ['a']
print(add_item_good("b"))  # ['b']


# 2. `is` vs `==`: identity vs equality
a = [1, 2, 3]
b = [1, 2, 3]
c = a
print(a == b)  # True: same values
print(a is b)  # False: different objects in memory
print(a is c)  # True: c is just another name for a
# Only use `is` for singletons: `x is None`, `x is True`


# 3. Variables are names pointing to objects (assignment never copies)
original = [1, 2, 3]
alias = original
alias.append(4)
print(original)  # [1, 2, 3, 4] - both names point to the same list


# 4. Shallow vs deep copy
nested = [[1, 2], [3, 4]]
shallow = copy.copy(nested)    # Same as nested.copy() or nested[:]
deep = copy.deepcopy(nested)

nested[0].append(99)
print(shallow)  # [[1, 2, 99], [3, 4]] - inner lists are shared!
print(deep)     # [[1, 2], [3, 4]]     - fully independent


# 5. Building a 2D list with * shares the inner list
grid_bad = [[0] * 3] * 3
grid_bad[0][0] = 1
print(grid_bad)   # [[1, 0, 0], [1, 0, 0], [1, 0, 0]]

grid_good = [[0] * 3 for _ in range(3)]
grid_good[0][0] = 1
print(grid_good)  # [[1, 0, 0], [0, 0, 0], [0, 0, 0]]


# 6. Late binding in closures: the variable is looked up when called, not when defined
funcs_bad = [lambda: i for i in range(3)]
print([f() for f in funcs_bad])   # [2, 2, 2]

funcs_good = [lambda i=i: i for i in range(3)]  # Default arg captures the current value
print([f() for f in funcs_good])  # [0, 1, 2]


# 7. Modifying a list while looping over it skips items
numbers = [1, 2, 2, 3, 4]
for n in numbers:
    if n == 2:
        numbers.remove(n)
print(numbers)  # [1, 2, 3, 4] - one 2 survived!

numbers = [1, 2, 2, 3, 4]
numbers = [n for n in numbers if n != 2]  # Build a new list instead
print(numbers)  # [1, 3, 4]


# 8. Integer division and floating point
print(7 / 2)    # 3.5 (always a float)
print(7 // 2)   # 3   (floor division)
print(-7 // 2)  # -4  (floors towards negative infinity, not towards zero!)
print(0.1 + 0.2 == 0.3)  # False
import math
print(math.isclose(0.1 + 0.2, 0.3))  # True


# 9. *args and **kwargs
def describe(*args, **kwargs):
    print(f"args={args}, kwargs={kwargs}")  # args is a tuple, kwargs is a dict


describe(1, 2, name="Ana", age=30)
values = [1, 2]
options = {"sep": " | "}
print(*values, **options)  # Unpacking: same as print(1, 2, sep=" | ")


# 10. Truthiness: empty things are False
for value in [0, "", [], {}, None, 0.0]:
    assert not value
print("All empty values are falsy")
