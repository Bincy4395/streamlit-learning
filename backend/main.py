from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()


class ChatRequest(BaseModel):
    messages: list
    model: str
    temperature: float
    max_tokens: int


@app.get("/")
def home():
    return {
        "message": "AI Backend is running"
    }


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
            "stream": False
        }
    )

    if response.status_code != 200:
        return {
            "status": response.status_code,
            "ollama_error": response.text
        }

    response.raise_for_status()

    data = response.json()

    return {
        "response": data["message"]["content"]
    }