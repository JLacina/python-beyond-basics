"""
Call a Hugging Face AI model over plain HTTP with the requests library.

Hugging Face provides open-source AI models, with limited free usage (requires an account and API key).
https://huggingface.co/docs/inference-providers/guides/first-api-call

Setup: create an access token on huggingface.co and save it in examples/secrets/hf.txt
(the secrets/ folder is in .gitignore so the key is never committed).

Compare with example_11_hf_api_library.py, which does the same thing with the official library.
"""
import requests

API_URL = "https://router.huggingface.co/v1/chat/completions"
DEFAULT_MODEL = "meta-llama/Llama-3.2-3B-Instruct"


def load_api_key(path="secrets/hf.txt"):
    """Read the API key from a file that is NOT committed to git."""
    try:
        with open(path, encoding="utf-8") as file:
            api_key = file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Save your Hugging Face token in {path} (see the docstring at the top)") from None
    if not api_key:
        raise ValueError(f"{path} is empty - paste your Hugging Face token into it")
    return api_key


def query_huggingface_ai(message, api_key, model=DEFAULT_MODEL):
    """Send one user message to the model and return its reply as a string."""
    headers = {"Authorization": f"Bearer {api_key}"}  # Bearer token authentication

    payload = {  # OpenAI-compatible "chat completions" format
        "messages": [
            {
                "role": "user",
                "content": message,
            }
        ],
        "model": model,
    }
    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()  # e.g. 401 = bad token, 429 = free quota used up

    data = response.json()
    return data["choices"][0]["message"]["content"]  # Dig into the nested JSON response


if __name__ == "__main__":
    prompt = "Hello, world!"
    print(query_huggingface_ai(prompt, load_api_key()))
