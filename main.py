from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from db import db


logging.basicConfig(
    level=logging.INFO,
    format="{asctime} [{levelname}] {message}",
    style="{",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        db.QDRANT_CLIENT = db.qdrant_client_connect()
        db.ensure_collections(db.QDRANT_CLIENT)
    except Exception as e:
        logging.error(f"Startup failed: {e}")
        raise
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def home():
    return {"status": "ok"}
