import re


def split_explanation_and_code(text):
    code_pattern = re.compile(r"```python\s*(.*?)\s*```", re.DOTALL)

    parts = []
    last_end = 0
    # Iterate over each code block found.
    for match in code_pattern.finditer(text):
        # Everything before the current code block is explanation text.
        explanation = text[last_end : match.start()]
        if explanation.strip():  # Only add if there's non-whitespace text.
            parts.append(("explanation", explanation.strip()))

        # The captured group is the code snippet.
        code = match.group(1)
        if code.strip():
            parts.append(("code", code.strip()))

        last_end = match.end()

    # Any remaining text after the last code block.
    if last_end < len(text):
        explanation = text[last_end:]
        if explanation.strip():
            parts.append(("explanation", explanation.strip()))

    return parts


def make_pretty_print(user, color, is_bold, console, timezone):
    boldness = "bold" if is_bold else "not bold"

    console.rule(
        f"[{boldness} {color}]({user})[/{boldness} {color}] - "
        f"[{boldness} {color}][{timezone}][/{boldness} {color}]"
    )
