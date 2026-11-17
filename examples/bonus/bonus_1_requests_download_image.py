"""
Download an image (binary data) with requests and save it to image.png.

- stream=True downloads the body in chunks instead of loading it all into memory first
- Open the file in "wb" (write binary) mode, because images are bytes, not text
- shutil.copyfileobj copies from the response stream straight into the file
"""
import shutil

import requests

URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Flag_of_Canada_%28Pantone%29.svg/60px-Flag_of_Canada_%28Pantone%29.svg.png"

headers = {"User-Agent": "Your name (your@email.com)"}  # Wikimedia blocks requests without a User-Agent
response = requests.get(URL, headers=headers, stream=True, timeout=10)

response.raise_for_status()  # Stop here with an HTTPError if the download failed

with open("image.png", "wb") as f:
    response.raw.decode_content = True  # Un-gzip the data if the server compressed it
    shutil.copyfileobj(response.raw, f)
