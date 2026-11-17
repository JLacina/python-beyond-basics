"""
Scrape UN member states from Wikipedia and save them to countries.csv.

Stage B of the project: like stage A, but also collect the date each country joined,
store each country as a dict, and write the result as a CSV with csv.DictWriter.
"""

import csv

import requests
from bs4 import BeautifulSoup


URL = "https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations"
HEADERS = {"User-Agent": "python-beyond-basics scraper"}  # Wikipedia blocks requests with no User-Agent


def find_member_table(soup: BeautifulSoup):
    """Return the one table with class 'wikitable', or raise ValueError if the page layout changed."""
    tables = soup.find_all("table", class_="wikitable")

    # Use exceptions, not assert, for runtime checks: asserts are removed when Python runs with -O
    if len(tables) > 1:
        raise ValueError("Found more than one table with class 'wikitable'")
    if len(tables) == 0:
        raise ValueError("Could not find UN member states table with class 'wikitable'")

    return tables[0]


def scrape_countries() -> list[dict[str, str]]:
    """Download the Wikipedia page and return [{"Name": ..., "Date Joined": ...}, ...]."""
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()  # Raise requests.HTTPError for 4xx/5xx responses

    soup = BeautifulSoup(response.text, "html.parser")
    table = find_member_table(soup)

    countries: list[dict[str, str]] = []
    for row in table.find_all("tr")[1:]:  # [1:] skips the header row
        name = row.th.a.string
        date_joined = row.td.span.string  # First <td> holds the admission date
        country = {
            "Name": name,
            "Date Joined": date_joined,
        }
        countries.append(country)

    return countries


def save_countries(countries: list[dict[str, str]]) -> None:
    """Write the countries to countries.csv with a header row."""
    # newline="" stops the csv module writing blank lines between rows on Windows
    with open("countries.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Date Joined"])
        writer.writeheader()
        writer.writerows(countries)


if __name__ == "__main__":
    countries_list = scrape_countries()
    save_countries(countries_list)
