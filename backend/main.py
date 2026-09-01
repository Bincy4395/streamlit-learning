from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import requests
import json

app = FastAPI()


# -----------------------------
# Request Schema
# -----------------------------

class ChatRequest(BaseModel):
    messages: list
    model: str
    temperature: float
    max_tokens: int


# -----------------------------
# Home
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "AI Backend is running"
    }


# -----------------------------
# Chat - Streaming
# -----------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": request.model,
            "messages": request.messages,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_tokens
            },
            "stream": True
        },
        stream=True
    )

    # -----------------------------
    # Ollama Error Handling
    # -----------------------------

    if response.status_code != 200:
        return {
            "status": response.status_code,
            "ollama_error": response.text
        }

    # -----------------------------
    # Generate Chunks
    # -----------------------------

    def generate():

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

    # -----------------------------
    # Return Streaming Response
    # -----------------------------

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )