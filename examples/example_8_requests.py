"""
Download a web page with the requests library.

`pip install requests`

Documentation: https://docs.python-requests.org/en/latest/index.html

Steps: send a GET request -> check the status code -> use the text -> save it to a file.
Always set a timeout, otherwise a slow server can make your program hang forever.
"""

import requests

URL = "https://automatetheboringstuff.com/3e/chapter13.html"

# Dictionary of HTTP headers
headers = {"User-Agent": "your@email.com"}  # Metadata for request: tells the site who you are
params = {"param1": 123, "param2": 456}     # Adds ?param1=123&param2=456 to URL

response = requests.get(URL, params=params, headers=headers, timeout=10)

# Full list of HTTP status codes: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
# Common status codes:
# - 200 OK
# - 401 Unauthorized
# - 404 Not found
# - 502 Bad gateway
print(response.status_code)
print(response.reason)

# Raise exception (requests.HTTPError) if the status code is 4xx or 5xx
response.raise_for_status()

# Get text contents
print(response.text)

with open("data/request.html", "w", encoding="utf-8") as file:
    file.write(response.text)
