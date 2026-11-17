"""
Find the 10 most common words in data/google.html's visible text,
ignoring case and punctuation.
"""
import re
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

html_path = Path(__file__).parent.parent / "data" / "google.html"

with open(html_path, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file.read(), "html.parser")

for tag in soup(["script", "style"]):  # Remove code so we only count visible text
    tag.decompose()

text = soup.get_text(" ")

words = re.findall(r"[a-z]+", text.lower())  # Letters only, already lowercase
counts = Counter(words)

for word, count in counts.most_common(10):
    print(f"{word}: {count}")
