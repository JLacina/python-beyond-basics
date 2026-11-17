"""
Read a CSV file with csv.DictReader.

DictReader uses the first row (the header) as keys, so each row is a dict:
{"Country": "Canada", "Capital": "Ottawa"}
Open CSV files with newline="" - the csv module handles line endings itself.
"""
import csv

with open("data/input.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for country in reader:
        print(f'The capital of {country["Country"]} is {country["Capital"]}')
