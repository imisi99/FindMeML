import os
import logging
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


VECTOR_SIZE = 768
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
QDRANT_CLIENT = QdrantClient


def qdrant_client_connect() -> QdrantClient:
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    return client


def ensure_collections(client: QdrantClient):
    collections = client.get_collections().collections
    existing = {c.name for c in collections}

    if "users" not in existing:
        client.create_collection(
            collection_name="users",
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        logging.info("[QDRANT] Created users collections as it did not exist.")

    if "projects" not in existing:
        client.create_collection(
            collection_name="projects",
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        logging.info("[QDRANT] Created projects collections as it did not exist.")


def get_qdrant_client():
    """Returns a pre-initialized qdrant client"""
    return QDRANT_CLIENT
