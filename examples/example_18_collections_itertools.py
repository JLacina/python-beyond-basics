"""
Standard library power tools: collections and itertools.
Interview tip: Counter, defaultdict and deque solve many coding problems in one line.
Also know the Big-O of the built-in data structures (bottom of this file).
"""
from collections import Counter, defaultdict, deque, namedtuple
from itertools import chain, combinations, groupby, permutations, product

# Counter: count things
text = "the quick brown fox jumps over the lazy dog the end"
word_counts = Counter(text.split())
print(word_counts.most_common(2))  # [('the', 3), ('quick', 1)]
print(word_counts["the"])          # 3
print(word_counts["missing"])      # 0 (no KeyError)

# Classic interview question: are two words anagrams?
print(Counter("listen") == Counter("silent"))  # True

# defaultdict: missing keys get a default value automatically
words = ["apple", "avocado", "banana", "blueberry", "cherry"]
by_letter = defaultdict(list)
for word in words:
    by_letter[word[0]].append(word)  # No need to check if the key exists
print(dict(by_letter))

# deque: fast appends/pops from BOTH ends (list.pop(0) is O(n), deque.popleft() is O(1))
queue = deque([1, 2, 3])
queue.append(4)        # Add to the right
queue.appendleft(0)    # Add to the left
print(queue.popleft()) # 0
print(queue)           # deque([1, 2, 3, 4])

recent = deque(maxlen=3)  # Keeps only the last 3 items
for i in range(10):
    recent.append(i)
print(recent)  # deque([7, 8, 9], maxlen=3)

# namedtuple: a lightweight, immutable record
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y, p)

# itertools
print(list(chain([1, 2], [3, 4])))           # [1, 2, 3, 4] - join iterables
print(list(combinations("ABC", 2)))          # [('A','B'), ('A','C'), ('B','C')] - order doesn't matter
print(list(permutations("ABC", 2)))          # 6 pairs - order matters
print(list(product([0, 1], repeat=2)))       # [(0,0), (0,1), (1,0), (1,1)] - like nested loops

# groupby: groups CONSECUTIVE items, so sort first!
animals = ["cat", "dog", "cow", "duck", "cobra"]
for letter, group in groupby(sorted(animals), key=lambda a: a[0]):
    print(letter, list(group))

# zip and enumerate (built-ins, but essential)
names = ["Ana", "Ben"]
ages = [30, 25]
for i, (name, age) in enumerate(zip(names, ages), start=1):
    print(f"{i}. {name} is {age}")


# Big-O cheat sheet
# list:  index O(1), append O(1), pop() O(1), pop(0)/insert(0) O(n), `in` O(n), sort O(n log n)
# dict:  get/set/delete O(1), `in` O(1)
# set:   add/remove O(1), `in` O(1)  <- convert a list to a set if you check membership a lot
# deque: append/appendleft/pop/popleft O(1), index O(n)

big_list = list(range(1_000_000))
big_set = set(big_list)
print(999_999 in big_list)  # Scans the whole list: slow
print(999_999 in big_set)   # Hash lookup: instant
