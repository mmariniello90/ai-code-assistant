# ai-code-assistant 

`ai-code-assistant`  is a lightweight AI-powered Python assistant that utilizes an LLM (deepseek-coder-v2) to assist users in generating, explaining, and formatting Python code. The assistant maintains a conversational history, highlights syntax for better readability, and provides structured responses.

## Features

- **Interactive Chat**: Engage in a back-and-forth conversation with the AI to get Python-related assistance.
- **Code Explanation and Formatting**: The assistant intelligently separates explanations from code and highlights syntax using `rich`.
- **Conversation History**: Maintains context to ensure meaningful interactions.
- **Simple Command-line Interface**: Designed for ease of use with a clean terminal-based UI.
- **Private and local experience**: Thought to run in you local terminal, without sharing your code with third-parties.

## Installation

### Prerequisites
- Python 3.11+
- `ollama` library for LLM-based chat
- `colorama` for colored terminal output
- `rich` for syntax highlighting

Install the dependencies:

Using poetry:
```
poetry add ollama colorama pygments
```
Or using pip:
```sh
pip install ollama colorama pygments
```

## Usage

Run the assistant from the terminal:
```sh
python app/assistant.py
```

### Commands
- Start typing to interact with the AI.
- Type `quit` to exit the session.

## How It Works

1. Initializes with a **system prompt** to define AI behavior.
2. Maintains **message history** for a better conversational experience.
3. Uses `ollama.chat` to generate AI responses.
4. Processes AI responses to **separate explanations from code snippets**.
5. Formats and highlights code snippets for better readability.
6. Prints responses in a color-coded format (`colorama`).

## Example Interaction

```
[AI]
Hi, how can I help with?

[USER]
Write a function to check if a number is prime.

[AI]
Here's a Python function to check for a prime number:

--------------------------------------------------------------------------------
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
--------------------------------------------------------------------------------

You can use `is_prime(7)` to test it.
```

## Configuration

Modify the **model settings** in `model/config.py`:
```python
MODEL_NAME = "your-model-name"
SYSTEM_PROMPT = "your-system-prompt"
```


