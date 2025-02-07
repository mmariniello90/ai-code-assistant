from ollama import chat
from colorama import Fore, Style
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

from model.config import MODEL_NAME, SYSTEM_PROMPT
from utils.format_text import split_explanation_and_code


def main():
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "assistant",
            "content": "Hi, how can I help with?",
        },
    ]

    print(Fore.RED + f"[AI]" + Style.RESET_ALL)
    print(messages[1]["content"])
    print()

    while True:
        print(Fore.GREEN + "[USER]" + Style.RESET_ALL)
        user_input = input()
        print()

        if user_input.strip() == "quit":
            break

        response = chat(
            MODEL_NAME,
            messages=messages
            + [
                {"role": "user", "content": user_input},
            ],
        )

        # Add the response to the messages to maintain the history
        messages += [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": response.message.content},
        ]

        print(Fore.RED + f"[AI]" + Style.RESET_ALL)

        generation = split_explanation_and_code(response.message.content)

        for content in generation:
            if content[0] == "explanation":
                print(content[-1])
                print()
            else:
                print("--" * 40)

                colored_code = highlight(
                    content[-1], PythonLexer(), TerminalFormatter()
                )

                print(colored_code)
                print("--" * 40)
                print()


if __name__ == "__main__":
    main()
