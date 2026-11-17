"""
Scrape UN member states from Wikipedia, visit each country's page for its
coordinates, and save everything to countries_more.csv.

Stage C of the project: follow the link in each row to a second page and pull extra
data from it. That means one request per country (~190), so `limit` lets you test on
a few countries first - be polite to the server you are scraping.
"""

import csv

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://en.wikipedia.org"
URL = BASE_URL + "/wiki/Member_states_of_the_United_Nations"
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
    """Download the list page and return [{"Name", "Date Joined", "URL"}, ...]."""
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = find_member_table(soup)

    countries: list[dict[str, str]] = []
    for row in table.find_all("tr")[1:]:  # [1:] skips the header row
        name = row.th.a.string
        date_joined = row.td.span.string
        url = row.th.a['href']  # Relative link, e.g. "/wiki/Canada"
        country = {
            "Name": name,
            "Date Joined": date_joined,
            "URL": url,
        }
        countries.append(country)

    return countries


def get_country_data(countries: list[dict[str, str]], limit: int | None = 3) -> list[dict[str, str]]:
    """Add "Latitude" and "Longitude" to the first `limit` countries (None = all of them)."""
    for country in countries[:limit]:  # countries[:None] is the whole list
        country_url = f"{BASE_URL}{country['URL']}"
        response = requests.get(country_url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        latitude = soup.find("span", class_="latitude")    # find() returns None if not found...
        longitude = soup.find("span", class_="longitude")
        if latitude is None or longitude is None:          # ...so check BEFORE using .string
            print(f"Could not find latitude or longitude for {country['Name']}")
            continue
        country["Latitude"] = latitude.string
        country["Longitude"] = longitude.string

    return countries


def save_countries(countries: list[dict[str, str]]) -> None:
    """Write all countries to countries_more.csv (missing coordinates become empty cells)."""
    # newline="" stops the csv module writing blank lines between rows on Windows
    with open('countries_more.csv', "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Date Joined", "Latitude", "Longitude", "URL"])
        writer.writeheader()
        writer.writerows(countries)


if __name__ == "__main__":
    countries_list = scrape_countries()
    countries_list = get_country_data(countries_list)  # Pass limit=None to fetch every country
    save_countries(countries_list)
