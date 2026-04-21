# OmniTask API

A secure task management backend built with FastAPI.

## Features

- JWT Authentication
- User registration and login
- Task CRUD operations
- Pagination and filtering
- Task search
- Overdue task detection
- Unit testing
- Docker support

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- Pytest
- Docker

## Setup

Install dependencies:

pip install -r requirements.txt

Run server:

uvicorn main:app --reload

API docs:

http://127.0.0.1:8000/docs

## Authentication

Login endpoint returns JWT token.

Use token in requests:

Authorization: Bearer <token>

## Docker

Build container:

docker build -t omnitask .

Run container:

docker run -p 8000:8000 omnitask

## Testing

Run tests:

pytest
