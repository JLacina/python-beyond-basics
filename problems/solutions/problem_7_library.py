"""
Model a small library system with classes.
"""
from dataclasses import dataclass


@dataclass
class Book:
    title: str
    author: str
    is_checked_out: bool = False


class BookNotAvailableError(Exception):
    pass


class Library:
    def __init__(self):
        self._books: dict[str, Book] = {}

    def add_book(self, book: Book) -> None:
        self._books[book.title] = book

    def checkout(self, title: str) -> Book:
        book = self._books.get(title)
        if book is None:
            raise BookNotAvailableError(f"We don't have {title!r}")
        if book.is_checked_out:
            raise BookNotAvailableError(f"{title!r} is already checked out")
        book.is_checked_out = True
        return book

    def return_book(self, title: str) -> None:
        self._books[title].is_checked_out = False

    @property
    def available(self) -> list[Book]:
        return [book for book in self._books.values() if not book.is_checked_out]

    def __len__(self) -> int:
        return len(self._books)

    def __contains__(self, title: str) -> bool:
        return title in self._books


library = Library()
library.add_book(Book("1984", "George Orwell"))
library.add_book(Book("Jane Eyre", "Charlotte Brontë"))

assert len(library) == 2
assert "1984" in library
assert "Dune" not in library

library.checkout("1984")
assert [book.title for book in library.available] == ["Jane Eyre"]

try:
    library.checkout("1984")
    assert False, "Should have raised an error"
except BookNotAvailableError as e:
    print(f"Error as expected: {e}")

library.return_book("1984")
assert len(library.available) == 2
print("All checks passed")
