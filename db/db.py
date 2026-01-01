import os
import logging
from typing import Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


VECTOR_SIZE = 768
QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
QDRANT_CLIENT: Optional[QdrantClient] = None


def qdrant_client_connect() -> QdrantClient:
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    return client


def ensure_collections(client: QdrantClient):
    collections = client.get_collections().collections
    existing = {c.name for c in collections}

    if "users" not in existing:
        logging.info("[QDRANT] Creating users collections as it did not exist.")

        try:
            client.create_collection(
                collection_name="users",
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
            )
        except Exception as e:
            logging.error("[QDRANT] Failed to create the users collection -> %s", e)
        logging.info("[QDRANT] Users collection created.")

    if "projects" not in existing:
        logging.info("[QDRANT] Creating projects collections as it did not exist.")

        try:
            client.create_collection(
                collection_name="projects",
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
            )
        except Exception as e:
            logging.error("[QDRANT] Failed to create the project collection. -> %s", e)
            raise
        logging.info("[QDRANT] Projects collection created.")


def get_qdrant_client() -> QdrantClient:
    """Returns a pre-initialized qdrant client"""
    if QDRANT_CLIENT is None:
        raise RuntimeError("[QDRANT] Qdrant Client not initialized.")
    return QDRANT_CLIENT
