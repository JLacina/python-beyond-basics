"""
Classes and OOP: attributes, methods, dunder methods, properties, inheritance, dataclasses.
Interview tip: know the difference between instance, class and static methods,
and when a @dataclass saves you from writing boilerplate.
"""
from dataclasses import dataclass, field


# Basic class
class BankAccount:
    interest_rate = 0.02  # Class attribute: shared by all instances

    def __init__(self, owner, balance=0):
        self.owner = owner        # Instance attributes: unique to each object
        self._balance = balance   # Leading underscore = "private by convention"

    # Property: access like an attribute, but runs code
    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount

    # Class method: gets the class (cls), often used as an alternative constructor
    @classmethod
    def from_string(cls, text):
        owner, balance = text.split(",")
        return cls(owner, float(balance))

    # Static method: doesn't need the instance or class, just grouped here logically
    @staticmethod
    def is_valid_amount(amount):
        return amount > 0

    # Dunder (double underscore) methods hook into Python's built-in behaviour
    def __repr__(self):  # Used by repr(), the debugger and the REPL - aim for "unambiguous"
        return f"BankAccount(owner={self.owner!r}, balance={self._balance})"

    def __str__(self):   # Used by print() and str() - aim for "readable"
        return f"{self.owner}'s account: ${self._balance:,.2f}"

    def __eq__(self, other):
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.owner == other.owner and self._balance == other._balance


account = BankAccount("Ana", 100)
account.deposit(50)
print(account)          # Ana's account: $150.00   (__str__)
print(repr(account))    # BankAccount(owner='Ana', balance=150)   (__repr__)
print(account.balance)  # 150 (property - no brackets)

try:
    account.balance = 1_000_000  # Read-only property, no setter
except AttributeError as e:
    print(f"Can't do that: {e}")

account_2 = BankAccount.from_string("Ben,250.5")
print(account_2)
print(BankAccount.is_valid_amount(-5))  # False
print(BankAccount("Ana", 150) == account)  # True (__eq__)


# Inheritance: SavingsAccount IS-A BankAccount
class SavingsAccount(BankAccount):
    interest_rate = 0.05  # Override class attribute

    def __init__(self, owner, balance=0, min_balance=100):
        super().__init__(owner, balance)  # Call the parent's __init__
        self.min_balance = min_balance

    def withdraw(self, amount):  # Override a method
        if self._balance - amount < self.min_balance:
            raise ValueError(f"Must keep at least ${self.min_balance}")
        super().withdraw(amount)

    def add_interest(self):
        self._balance += self._balance * self.interest_rate


savings = SavingsAccount("Cleo", 1000)
savings.add_interest()
print(savings)  # Cleo's account: $1,050.00 (inherited __str__)
print(isinstance(savings, BankAccount))  # True
print(SavingsAccount.__mro__)  # Method Resolution Order: where Python looks for methods


# Dataclass: generates __init__, __repr__ and __eq__ for you
@dataclass
class Book:
    title: str
    author: str
    year: int
    tags: list[str] = field(default_factory=list)  # Never use a mutable default like `= []`

    @property
    def is_classic(self):
        return self.year < 1950


book = Book("1984", "George Orwell", 1949)
print(book)              # Book(title='1984', author='George Orwell', year=1949, tags=[])
print(book.is_classic)   # True
print(book == Book("1984", "George Orwell", 1949))  # True


# Frozen dataclass: immutable and hashable (can be a dict key or go in a set)
@dataclass(frozen=True)
class Point:
    x: float
    y: float


p = Point(1, 2)
print({p: "origin-ish"})
try:
    p.x = 5
except AttributeError as e:  # FrozenInstanceError is a subclass of AttributeError
    print(f"Frozen: {e}")
