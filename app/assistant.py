from ollama import chat
from rich.console import Console
from rich.syntax import Syntax
from rich.markdown import Markdown

from model.config import MODEL_NAME, SYSTEM_PROMPT
from utils.format_text import split_explanation_and_code


def main():
    console = Console()

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

    console.print("[bold magenta](AI)[/bold magenta]")
    print(messages[1]["content"])
    print()

    while True:
        console.print("[bold green](USER)[/bold green]")
        user_input = input()
        print()

        if user_input.strip() == "quit":
            console.print("[bold magenta](AI)[/bold magenta]")
            print("Bye!")
            break

        with console.status("[gray]Generating...", spinner="dots2"):
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

        console.print("[bold magenta](AI)[/bold magenta]")

        generation = split_explanation_and_code(response.message.content)

        for content in generation:
            if content[0] == "explanation":
                md = Markdown(content[-1])
                console.print(md)
                print()
            else:
                colored_code = Syntax(
                    content[-1], lexer="python", theme="monokai", line_numbers=True
                )

                console.print(colored_code)

                print()


if __name__ == "__main__":
    main()
