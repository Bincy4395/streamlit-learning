from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]

    model: str = Field(
        min_length=1
    )

    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0
    )

    max_tokens: int = Field(
        default=300,
        ge=50,
        le=1000
    )