"""
Scrape a page that requires you to log in.

How form logins usually work:
1. GET the login page - it contains a hidden CSRF/"authenticity" token
2. POST your username, password AND that token to the login URL
3. The site sets a session cookie. A requests.Session keeps cookies between requests,
   so every later request is made as the logged-in user.

Note: many sites (GitHub included) also use 2FA or bot protection, and scraping behind a
login may break their terms of service - prefer an official API where one exists.
"""
import requests
from bs4 import BeautifulSoup

LOGIN_URL = "https://github.com/session"
USERNAME = "***"  # Don't hard-code real credentials - see bonus_5_secrets.py
PASSWORD = "***"

URL = "https://github.com"
headers = {"User-Agent": "Your name (your@email.com)"}

# Create new session so that cookies are saved between requests
session_requests = requests.session()

# Get the authenticity token from the login page
login_page = session_requests.get(LOGIN_URL, headers=headers, timeout=10)
soup = BeautifulSoup(login_page.text, "html.parser")

# The input name might be different depending on the site. Inspect the form and look for a hidden input with "authenticity" or "csrf".
# Note: `name` is find()'s first parameter (the tag name), so the HTML name attribute must go in attrs
token_input = soup.find("input", attrs={"name": "authenticity_token"})
if token_input is None:
    raise RuntimeError("Could not find the authenticity token on the login page")
auth_token = token_input.get("value")
print(auth_token)

# Send login request
data = {
    "login": USERNAME,
    "password": PASSWORD,
    "authenticity_token": auth_token,
}
response = session_requests.post(LOGIN_URL, headers=headers, data=data, timeout=10)
print(response.status_code)

# Now you are authenticated and can start scraping the URL you want
response = session_requests.get(URL, headers=headers, timeout=10)

with open(
    "data/logged_in.html", "w", encoding="utf-8"
) as file:  # Open this to verify that your login worked
    file.write(response.text)

# ... Do some scraping with the result
