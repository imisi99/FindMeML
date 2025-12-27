from pydantic import BaseModel


class UserPayload(BaseModel):
    type: str = "user"
    id: str
    active: bool = True


class UserEmbeddingInput(BaseModel):
    id: str
    bio: str
    skills: list[str]
    interests: list[str]
