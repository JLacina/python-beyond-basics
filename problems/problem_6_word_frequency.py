"""
Find the 10 most common words in data/google.html's visible text,
ignoring case and punctuation.
Practises: BeautifulSoup, comprehensions, Counter
"""
from bs4 import BeautifulSoup

with open("data/google.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file.read(), "html.parser")

text = soup.get_text()

# Todo: Split text into lowercase words (letters only)

# Todo: Count the words

# Todo: Print the 10 most common as "word: count"
