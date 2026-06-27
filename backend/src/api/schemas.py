from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class ChatRequest(BaseModel):
    messages: list[dict[str, str]] = Field(..., description="История сообщений")
    temperature: float = Field(0.7, ge=0.2, le=1.2)
    max_tokens: int = Field(200, ge=50, le=500)
    system_prompt: str = Field(
        "Ты полезный ассистент. Отвечай кратко и по делу."
    )
    model: str | None = None


class ChatMessage(BaseModel):
    role: str  # "user" или "assistant"
    content: str
