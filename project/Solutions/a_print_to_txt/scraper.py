"""
Scrape UN member states from Wikipedia and save them to countries.txt.

Stage A of the project: fetch the page -> find the table -> pull out each country name
-> write one name per line to a text file.
"""
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


def scrape_countries() -> list[str]:
    """Download the Wikipedia page and return the list of country names."""
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()  # Raise requests.HTTPError for 4xx/5xx responses

    soup = BeautifulSoup(response.text, "html.parser")
    table = find_member_table(soup)

    countries: list[str] = []
    for row in table.find_all("tr")[1:]:  # [1:] skips the header row
        name = row.th.a.string            # Each row: <th><a>Country name</a></th>

        countries.append(name)

    return countries


def save_countries(countries: list[str]) -> None:
    """Write one country per line to countries.txt."""
    with open("countries.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(countries))


if __name__ == "__main__":
    countries_list = scrape_countries()
    save_countries(countries_list)
