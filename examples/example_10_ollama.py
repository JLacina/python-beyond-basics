"""
Run a free AI model on your own computer with Ollama.

Documentation: https://github.com/ollama/ollama-python

Setup:
1. Install Ollama from https://ollama.com and make sure it is running
2. Download the model:  ollama pull llama3.2
3. pip install ollama

If Ollama isn't running you'll get a ConnectionError.
"""
import ollama

# Use generate() for one-shot prompts
response = ollama.generate(prompt="Hello, world", model="llama3.2")
print(response.response)

# Use chat() for messages w/ context
prompt = "Write a hello world script in python"

messages = [{"role": "user", "content": prompt}]
response: ollama.ChatResponse = ollama.chat(
    model="llama3.2", messages=messages
)

print(response["message"]["content"])  # Access via keys
print(response.message.content)        # Access via attributes
