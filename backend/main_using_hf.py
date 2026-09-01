from fastapi import FastAPI
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os


# -----------------------------
# Load environment variables
# -----------------------------

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

print("HF TOKEN:", HF_TOKEN)


# -----------------------------
# Hugging Face client
# -----------------------------

client = InferenceClient(
    api_key=HF_TOKEN
)


# -----------------------------
# FastAPI app
# -----------------------------

app = FastAPI()


# -----------------------------
# Request schema
# -----------------------------

class ChatRequest(BaseModel):
    message: str


# -----------------------------
# Home endpoint
# -----------------------------

@app.get("/")
def home():

    return {
        "message": "AI Backend is running"
    }


# -----------------------------
# Chat endpoint
# -----------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": request.message
            }
        ]
    )

    assistant_message = response.choices[0].message.content

    return {
        "response": assistant_message
    }