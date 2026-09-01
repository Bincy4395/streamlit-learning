import json
import requests

from backend.config import OLLAMA_URL


def stream_chat(
    messages: list,
    model: str,
    temperature: float,
    max_tokens: int
):

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
            timeout=120
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

        for line in response.iter_lines():

            if line:

                data = json.loads(line)

                content = data.get(
                    "message",
                    {}
                ).get(
                    "content"
                )

                if content:
                    yield content

    finally:

        response.close()