***FindMe ML Service*** 
A gRPC-based machine learning service for generating embeddings and powering the recommendation
system in FindMe. Uses Ollama for embedding generation and Qdrant for vector storage.

## Overview 

This service handles:
- User profile embeddings (bio, skills, interests)
- Project embeddings (title, description, required skills)

# Tech Stack
- **Python** - Core service implementation
- **gRPC** - Communication protocol with the Go backend
- **Ollama** - Local embedding generation using `nomic-embed-text`
- **Qdrant** - Vector database for storage
