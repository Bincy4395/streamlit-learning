import json
import requests

from backend.config import OLLAMA_URL


def stream_chat(
    messages: list,
    model: str,
    temperature: float,
    max_tokens: int
):
    messages = [
        {
            "role": message.role,
            "content": message.content
        }
        for message in messages
    ]

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "messages": messages,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                },
                "stream": True
            },
            stream=True,
            timeout=(10, 180)
        )

        response.raise_for_status()

    except requests.exceptions.ConnectionError:

        raise RuntimeError(
            "Cannot connect to Ollama. "
            "Make sure Ollama is running."
        )

    except requests.exceptions.Timeout:

        raise RuntimeError(
            "Ollama request timed out."
        )

    except requests.exceptions.HTTPError as e:

        raise RuntimeError(
            f"Ollama returned an HTTP error: {e}"
        )


    try:

        for line in response.iter_lines(
            decode_unicode=True
        ):

            if not line:
                continue

            try:

                data = json.loads(line)

            except json.JSONDecodeError:

                continue


            # -----------------------------------------
            # Ollama error
            # -----------------------------------------

            if "error" in data:

                raise RuntimeError(
                    data["error"]
                )


            # -----------------------------------------
            # Get response content
            # -----------------------------------------

            content = data.get(
                "message",
                {}
            ).get(
                "content",
                ""
            )


            if content:
                yield content


            # -----------------------------------------
            # Ollama finished
            # -----------------------------------------

            if data.get("done"):

                break

    finally:

        response.close()