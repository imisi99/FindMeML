from pydantic import BaseModel


class ProjectPayload(BaseModel):
    type: str = "project"
    id: str
    open: bool = True


class ProjectEmbeddingInput(BaseModel):
    id: str
    title: str
    description: str
    skills: list[str]
