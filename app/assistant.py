import click
from ollama import chat
from rich.console import Console
from rich.syntax import Syntax
from rich.markdown import Markdown

from model.config import MODEL_NAME, USER_NAME, SYSTEM_PROMPT, TIME_ZONE
from utils.format_text import split_explanation_and_code
from utils.get_local_time import get_local_time


@click.command()
@click.option('--model', type=str, default="deepseek-coder-v2", help='LLM name.')
@click.option('--user', type=str, default="user1", help='User name.')
@click.option('--timezone', type=str, default="Europe/Rome", help='Your timezone.')
@click.option('--temperature', type=float, default=0.7, help='Model temperature.')
@click.option('--num_predict', type=int, default=2000, help='Max tokens to predict.')
def main(model, user, timezone, temperature, num_predict):

    click.echo(f"MODEL NAME: {model}")
    click.echo(f"USER NAME: {user}")
    click.echo(f"TIMEZONE: {timezone}")
    click.echo(f"TEMPERATURE: {temperature}")
    click.echo(f"MAX TOKENS: {num_predict}")

    console = Console()

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "assistant",
            "content": f"Hi {user}, how can I help with?",
        },
    ]

    console.rule(
        f"[bold magenta]({model})[/bold magenta] - "
        f"[not bold magenta][{get_local_time(time_zone=timezone)}][/not bold magenta]"
    )
    print(messages[1]["content"])
    print("\n\n")

    while True:
        console.rule(
            f"[bold green]({user})[/bold green] - "
            f"[not bold green][{get_local_time(time_zone=timezone)}][/not bold green]"
        )
        user_input = input(">: ")
        print("\n\n")

        if user_input.strip() == "quit":
            console.rule(
                f"[bold magenta]({model})[/bold magenta] - "
                f"[not bold magenta][{get_local_time(time_zone=timezone)}][/not bold magenta]"
            )
            print("Bye!")
            print("\n\n")
            break

        with console.status("[gray]Generating...", spinner="dots2"):
            response = chat(
                model=model,
                options={
                    "temperature": temperature,
                    "num_predict": num_predict
                },
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

        console.rule(
            f"[bold magenta]({model})[/bold magenta] - "
            f"[not bold magenta][{get_local_time(time_zone=timezone)}][/not bold magenta]"
        )

        generation = split_explanation_and_code(response.message.content)

        for content in generation:
            if content[0] == "explanation":
                md = Markdown(content[-1])
                console.print(md)
                print("\n\n")
            else:
                colored_code = Syntax(
                    content[-1], lexer="python", theme="monokai", line_numbers=False
                )

                console.print(colored_code)
                print("\n\n")


if __name__ == "__main__":
    main()
