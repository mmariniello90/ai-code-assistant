from ollama import chat


def get_model_response(
    model: str, temperature: float, num_predict: int, history: list, user_input: str
):
    return chat(
        model=model,
        options={"temperature": temperature, "num_predict": num_predict},
        messages=history
        + [
            {"role": "user", "content": user_input},
        ],
    )
