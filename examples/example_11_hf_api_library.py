"""
Call a Hugging Face AI model using the official huggingface_hub library.

Hugging Face provides open-source AI models, with limited free usage (requires an account and API key).
https://huggingface.co/docs/inference-providers/guides/first-api-call

Setup:
1. pip install huggingface_hub
2. Create an access token on huggingface.co and save it in examples/secrets/hf.txt
   (the secrets/ folder is in .gitignore so the key is never committed)

The library builds the HTTP request for you - compare with example_11_hf_api_requests.py.
"""
from huggingface_hub import InferenceClient

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


def query_huggingface_ai(prompt, api_key, model=DEFAULT_MODEL):
    """Send one user message to the model and return its reply as a string."""
    client = InferenceClient(
        api_key=api_key,
    )

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return completion.choices[0].message.content  # Attributes instead of dict keys


if __name__ == "__main__":
    prompt = "Hello, world!"
    print(query_huggingface_ai(prompt, load_api_key()))
