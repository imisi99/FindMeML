import os
import requests

OLLAMA_EMBEDDING_HOST = os.getenv(
    "OLLAMA_EMBEDDING_HOST", "http://localhost:11434/api/embeddings"
)


def generate_vector_embedding(text: str) -> list[float]:
    """Generate embeddings using ollama nomic text embed model"""
    response = requests.post(
        OLLAMA_EMBEDDING_HOST,
        json={
            "model": "nomic-embed-text",
            "prompt": text,
        },
    )
    response.raise_for_status()
    return response.json()["embedding"]


def generate_user_embedding(
    bio: str, skills: list[str], interests: list[str]
) -> list[float]:
    """Generate embedding for a user profile"""
    text = f"""
    Bio: {bio}
    Skills: {", ".join(skills)}
    Interests: {", ".join(interests)}
    """.strip()
    return generate_vector_embedding(text)


def generate_project_embedding(
    title: str, description: str, skills: list[str]
) -> list[float]:
    """Generate embedding for a project"""
    text = f"""
    Title: {title}
    Description: {description}
    Required Skills: {", ".join(skills)}
    """.strip()
    return generate_vector_embedding(text)
