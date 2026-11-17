"""
Model a small library system with classes.
Practises: classes, @dataclass, @property, custom exceptions, dunder methods
"""

# Todo: Create a Book dataclass with title, author, and is_checked_out (default False)

# Todo: Create a custom exception BookNotAvailableError

# Todo: Create a Library class that:
#  - stores books in a dict keyed by title
#  - has add_book(book), checkout(title) and return_book(title) methods
#  - raises BookNotAvailableError when checking out a missing or checked-out book
#  - has an `available` property that returns a list of books not checked out
#  - supports len(library) and `"1984" in library` (hint: __len__ and __contains__)

# Todo: Test it with a few asserts
