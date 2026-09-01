from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from backend.schemas import ChatRequest
from backend.services.ollama_service import stream_chat


app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "AI Backend is running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    return StreamingResponse(
        stream_chat(
            messages=request.messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        ),
        media_type="text/plain"
    )