"""
Print the countries in ../examples/data/input.csv whose capital starts with the same
letter as the country (e.g. "Algeria: Algiers"), processing the file lazily.
"""
import csv
from pathlib import Path

csv_path = Path(__file__).parent.parent.parent / "examples" / "data" / "input.csv"


def read_rows(path):
    with open(path, newline="", encoding="utf-8") as file:
        yield from csv.DictReader(file)  # The file stays open until the generator finishes


def filter_rows(rows, condition):
    for row in rows:
        if condition(row):
            yield row


def format_rows(rows):
    for row in rows:
        yield f"{row['Country']}: {row['Capital']}"


def same_first_letter(row):
    return row["Country"][0] == row["Capital"][0]


rows = read_rows(csv_path)
matching = filter_rows(rows, same_first_letter)
lines = format_rows(matching)

for line in lines:  # Nothing is read from the file until this loop starts
    print(line)
