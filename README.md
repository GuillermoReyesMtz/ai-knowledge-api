# AI Knowledge API

A backend service built with FastAPI, PostgreSQL, SQLAlchemy, and Docker for storing and retrieving knowledge documents.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker

## Features

- Create documents
- Store data in PostgreSQL
- REST API endpoints
- Swagger/OpenAPI documentation

## Run locally

docker compose up -d

uvicorn app.main:app --reload

## API Docs

http://localhost:8000/docs

## Future Improvements

- Document search
- Embeddings with pgvector
- Semantic search
- Authentication
- CI/CD pipeline