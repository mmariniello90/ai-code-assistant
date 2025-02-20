import click
from rich.console import Console
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.prompt import Prompt

from model.prompts import system_prompt
from model.llms import get_model_response
from utils.format_text import split_explanation_and_code, make_pretty_print
from utils.get_local_time import get_local_time


@click.command()
@click.option("--model", type=str, default="deepseek-coder-v2", help="LLM name.")
@click.option("--user", type=str, default="user1", help="User name.")
@click.option("--timezone", type=str, default="Europe/Rome", help="Your timezone.")
@click.option("--temperature", type=float, default=0.7, help="Model temperature.")
@click.option("--num_predict", type=int, default=2000, help="Max tokens to predict.")
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
            "content": system_prompt,
        },
        {
            "role": "assistant",
            "content": f"Hi {user}, how can I help with?",
        },
    ]

    make_pretty_print(
        user=model,
        color="magenta",
        is_bold=True,
        timezone=get_local_time(time_zone=timezone),
        console=console,
    )

    # console.rule(
    #    f"[bold magenta]({model})[/bold magenta] - "
    #    f"[not bold magenta][{get_local_time(time_zone=timezone)}][/not bold magenta]"
    # )
    print(messages[1]["content"])
    print("\n\n")

    while True:
        make_pretty_print(
            user=user,
            color="green",
            is_bold=True,
            timezone=get_local_time(time_zone=timezone),
            console=console,
        )

        user_input = Prompt.ask(">: ")
        print("\n\n")

        if user_input.strip() == "quit":
            make_pretty_print(
                user=model,
                color="magenta",
                is_bold=True,
                timezone=get_local_time(time_zone=timezone),
                console=console,
            )

            print("Bye!")
            print("\n\n")
            break

        with console.status("[gray]Generating...", spinner="dots2"):

            response = get_model_response(
                model=model,
                temperature=temperature,
                num_predict=num_predict,
                history=messages,
                user_input=user_input
            )

        # Add the response to the messages to maintain the history
        messages += [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": response.message.content},
        ]

        make_pretty_print(
            user=model,
            color="magenta",
            is_bold=True,
            timezone=get_local_time(time_zone=timezone),
            console=console,
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
