# FindMe - Embedding Service

> A gRPC micro-service that generates and maintains vector embeddings for users
> and projects using Ollama and Qdrant.

---

## Overview

This service is part of the [FindMe](https://findmeapi.duckdns.org/swagger/index.html) micro-services architecture. It is responsible
for converting user profiles and project data into vector embeddings and storing
them in a Qdrant vector database. These embeddings power the recommendation
engine by enabling semantic similarity search across users and projects.

The service exposes two gRPC services — `UserEmbeddingService` and
`ProjectEmbeddingService` — and is called internally by the back-end service
whenever profile or project data changes.

---

## How It Works

1. The [back-end service](https://github.com/imisi99/FindMe) sends a gRPC request (create, update, status change, or delete) when user/project data changes.
2. This service formats the relevant fields into a structured text prompt and sends it to an Ollama instance running the `nomic-embed-text` model.
3. The resulting 768-dimensional vector is upserted into the appropriate Qdrant collection (`users` or `projects`) along with payload metadata.
4. The [recommendation service](https://github.com/imisi99/FindMeMLR) can then query these collections to find semantically similar users or projects.

```
Backend (Go)
    │ gRPC
    ▼
Embedding Service (Python)
    │ HTTP                  │ HTTP
    ▼                       ▼
Ollama (nomic-embed-text)  Qdrant (vector store)
```

---

## Embedding Strategy

**User vectors** are stored in the `users` collection under the `profile` named vector. The embedding is generated from a structured prompt combining:

- Bio
- Skills
- Interests

**Project vectors** are stored in the `projects` collection under the `description` named vector. The embedding is generated from:

- Title
- Description
- Required Skills

Both collections use **cosine similarity** with a vector size of **768 dimensions**.

---

## gRPC API

### UserEmbeddingService

| Method | Request | Description |
|---|---|---|
| `CreateUserEmbedding` | `UserEmbeddingRequest` | Generates and stores a new user vector |
| `UpdateUserEmbedding` | `UserEmbeddingRequest` | Regenerates the vector with updated profile data |
| `UpdateUserStatus` | `UpdateStatusRequest` | Updates the `status` payload field only (no re-embedding) |
| `DeleteUserEmbedding` | `DeleteEmbeddingRequest` | Removes the user vector from Qdrant |

### ProjectEmbeddingService

| Method | Request | Description |
|---|---|---|
| `CreateProjectEmbedding` | `ProjectEmbeddingRequest` | Generates and stores a new project vector |
| `UpdateProjectEmbedding` | `ProjectEmbeddingRequest` | Regenerates the vector with updated project data |
| `UpdateProjectStatus` | `UpdateStatusRequest` | Updates the `status` payload field only (no re-embedding) |
| `DeleteProjectEmbedding` | `DeleteEmbeddingRequest` | Removes the project vector from Qdrant |

gRPC server reflection is enabled, so you can inspect the API with tools like `grpcurl` or Postman.

---

## Tech Stack

| Concern | Technology |
|---|---|
| Language | Python 3.12 |
| gRPC Framework | `grpcio` 1.76.0 |
| Vector Database | Qdrant 1.16.3 |
| Embedding Model | `nomic-embed-text` via Ollama 0.13.5 |
| Containerization | Docker + Docker Compose |

---

## Project Structure

```
.
├── db/
│   └── db.py           # Qdrant client init and collection setup
├── generated/          # Auto-generated gRPC code (do not edit)
│   ├── emb_pb2.py
│   ├── emb_pb2_grpc.py
│   └── emb_pb2.pyi
├── model/
│   └── embedding.py    # Prompt construction and Ollama embedding logic
├── proto/
│   └── emb.proto       # Protobuf service definitions
├── services/
│   ├── user.py         # UserEmbeddingService implementation
│   └── project.py      # ProjectEmbeddingService implementation
├── docker-compose.yml
├── Dockerfile
├── generate.sh         # Proto code generation script
├── main.py             # Server entrypoint
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Docker & Docker Compose
- The `findme-shared-network` Docker network must exist

### Environment Variables

Create a `.env` file in the project root:

```env
OLLAMA_EMBEDDING_HOST=http://ollama:11434/api/embeddings
QDRANT_HOST=qdrant
QDRANT_PORT=6333
```

### Running with Docker Compose

```bash
# Create the shared network (only needed once)
docker network create findme-shared-network

# Start Qdrant, Ollama, and the embedding service
docker compose up -d --build
```

On first startup, Ollama won't have the embedding model yet. Pull it after the container is running:

```bash
docker exec -it findme_ollama ollama pull nomic-embed-text
```

The gRPC server will be available at `[::]:8000` on the shared network.

### Running Locally

```bash
pip install -r requirements.txt

# Generate proto files
chmod +x generate.sh && ./generate.sh

# Set env vars and run
OLLAMA_EMBEDDING_HOST=http://localhost:11434/api/embeddings \
QDRANT_HOST=localhost \
QDRANT_PORT=6333 \
python main.py
```

### Regenerating Proto Files

If you modify `proto/emb.proto`:

```bash
chmod +x generate.sh
./generate.sh
```

This regenerates the files in `generated/` and automatically fixes the relative import path in `emb_pb2_grpc.py`.

---

## Qdrant Collections

Collections are created automatically on startup if they don't exist.

| Collection | Vector Name | Size | Distance |
|---|---|---|---|
| `users` | `profile` | 768 | Cosine |
| `projects` | `description` | 768 | Cosine |

You can inspect the collections via the Qdrant dashboard at `http://localhost:6333/dashboard` when running locally.

---

## License

See [LICENSE](./LICENSE).
