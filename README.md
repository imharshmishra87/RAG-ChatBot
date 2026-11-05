<div align="center">

# 🎓 Course Simplifier — RAG ChatBot

**A Retrieval-Augmented Generation (RAG) system that summarises video content and lets users chat with it.**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-000000)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## 📖 Overview

**Course Simplifier** is a RAG-based backend designed to **summarise a given video and enable chat grounded in that video's content**. Instead of relying on a language model's general knowledge, the system retrieves the relevant portions of the video's content and uses them as context, so answers stay tied to the source material.

The project is built as a modular **FastAPI** service, with a clear separation between API routing, business logic, data models, validation, core infrastructure, and vector storage.

---

## ✨ Key Features

- **Video summarisation and content-grounded chat** — the core purpose of the system: summarise a video and answer questions based on its content.
- **Retrieval-Augmented Generation pipeline** — built on LangChain, with Google Gemini integrations, HuggingFace embedding tooling, and a Pinecone vector database client.
- **Modular, router-based API** — dedicated route modules for `chat`, `instructor`, `admin`, and `auth`.
- **Relational persistence** — SQLAlchemy models with tables created automatically on startup.
- **Automated background maintenance** — a scheduler runs an inactive-chat cleanup job every 5 minutes.
- **Application lifecycle management** — the scheduler is started and shut down cleanly through FastAPI's lifespan handler.
- **Health monitoring endpoint** — a `/health` route reports service status and version.

---

## 🏗️ Architecture

The application follows a layered structure, where each folder owns a distinct responsibility.

```
RAG-ChatBot/
├── app.py            # FastAPI entry point: app setup, router registration, lifespan, base routes
├── scheduler.py      # Background job scheduler configuration
├── Core/             # Core infrastructure (database engine and declarative base)
├── Model/            # Data models
├── Services/         # Business logic (includes inactive-chat cleanup)
├── Validation/       # Request/response validation
├── Vectordb/         # Vector database layer
├── routers/          # API route modules: chat, instructor, admin, auth
├── requirements.txt  # Pinned project dependencies
└── LICENSE           # MIT License
```

### Application Entry Point (`app.py`)

The service is a FastAPI application titled **"Course Simplifier"**. On startup it:

1. **Creates database tables** from the declarative models using the SQLAlchemy engine defined in `Core`.
2. **Registers four routers** — `chat`, `instructor`, `admin`, and `auth`.
3. **Starts the background scheduler** through an async lifespan context manager, and **shuts it down gracefully** when the application stops.

### Background Scheduler (`scheduler.py`)

An **APScheduler `BackgroundScheduler`** configured for the **Asia/Kolkata** timezone runs the `cleanup_inactive_chats` service as an **interval job every 5 minutes** (job id `CLIC_01`). This keeps stale chat sessions from accumulating without requiring any manual intervention.

---

## 🔌 API Endpoints

| Method | Endpoint  | Description                                                        |
|--------|-----------|--------------------------------------------------------------------|
| `GET`  | `/`       | Returns a welcome message for the Course Simplifier service.       |
| `GET`  | `/health` | Returns service status, version (`v1.0.0`), and application name.  |

Additional endpoints are provided by the `chat`, `instructor`, `admin`, and `auth` routers under `routers/`.

---

## 🧰 Technology Stack

The pinned dependencies in `requirements.txt` outline the stack:

| Area                       | Technologies                                                           |
|----------------------------|------------------------------------------------------------------------|
| **API Framework**          | FastAPI, Uvicorn, Pydantic, pydantic-settings, python-multipart        |
| **RAG / LLM Orchestration**| LangChain, LangChain Core, LangChain Community, LangSmith              |
| **LLM Provider**           | Google Gemini (`langchain-google-genai`, `google-genai`)               |
| **Embeddings**             | HuggingFace (`langchain-huggingface`, `sentence-transformers`, `transformers`) |
| **Vector Database**        | Pinecone                                                               |
| **Database & ORM**         | SQLAlchemy, Alembic, psycopg2                                          |
| **Security Utilities**     | python-jose (JWT), passlib with bcrypt                                 |
| **Scheduling**             | APScheduler                                                            |
| **Data & Utilities**       | NumPy, pandas, requests, aiohttp, python-dotenv                        |

---

## 🧠 How the RAG Approach Works

Retrieval-Augmented Generation combines a vector search layer with a language model:

1. **Content is converted into embeddings** and stored in a vector database.
2. **At question time, the most relevant content is retrieved** from the vector store.
3. **The language model answers using the retrieved context**, keeping responses grounded in the video's actual content rather than general knowledge.

In this project, the supporting pieces are declared in the stack above: HuggingFace embedding tooling, a Pinecone vector database client, and Google Gemini through LangChain, organised behind the `Vectordb` and `Services` layers.

---

## 🎯 Design Highlights

- **Separation of concerns** — routing, services, models, validation, core infrastructure, and vector storage each live in their own package.
- **Lifecycle-aware background jobs** — the scheduler is bound to the application lifespan rather than started ad hoc.
- **Pinned dependencies** — reproducible environments through version-pinned requirements.
- **Operational readiness** — a dedicated health endpoint for service monitoring.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built by [Harsh Mishra](https://github.com/imharshmishra87)**

</div>
