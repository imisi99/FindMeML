import requests
from schemas.project import ProjectEmbeddingInput
from schemas.user import UserEmbeddingInput


def user_text(user: UserEmbeddingInput) -> str:
    return f"""
    Skills: {", ".join(user.skills)}
    Bio: {user.bio}
    Interests: {", ".join(user.interests)}
    """.strip()


def project_test(project: ProjectEmbeddingInput) -> str:
    return f"""
    Titile: {project.title}
    Description: {project.description}
    Skills: {", ".join(project.skills)}
    """.strip()


def get_embeddings(text):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
    )
    return response.json()["embeddings"]
