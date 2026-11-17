"""Create text files for each letter that contain
all the countries that start with that letter
"""
from collections import defaultdict
from pathlib import Path
from pprint import pprint

countries_path = Path(__file__).parent.parent / "data" / "countries.txt"


def group_by_first_letter(lines) -> dict[str, list[str]]:
    """Return {letter: [countries]}, skipping blank lines."""
    country_letter_map = defaultdict(list)  # Missing keys start as an empty list
    for line in lines:
        country = line.strip()  # Strip FIRST, so blank lines become "" and get skipped
        if not country:
            continue
        country_letter_map[country[0].upper()].append(country)
    return dict(country_letter_map)


def write_letter_files(country_letter_map: dict[str, list[str]], folder: Path) -> None:
    """Write data/<letter>_countries.txt for each letter."""
    for letter, countries in country_letter_map.items():
        with open(folder / f"{letter}_countries.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(countries))


if __name__ == "__main__":
    with open(countries_path, "r", encoding="utf-8") as file:
        letter_map = group_by_first_letter(file)  # A file is an iterable of lines

    pprint(letter_map)
    write_letter_files(letter_map, countries_path.parent)
