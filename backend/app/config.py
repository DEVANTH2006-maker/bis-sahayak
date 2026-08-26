"""Application configuration — reads from environment variables."""

from __future__ import annotations

import os
from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- LLM ---
    # Options: "ollama" (free, local) | "gemini" (free tier) | "openai" | "anthropic"
    LLM_PROVIDER: str = "ollama"

    # Ollama (free, local — no API key needed)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"

    # Google Gemini free tier (15 RPM, 1M tokens/day)
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # OpenAI (paid — fallback only)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Anthropic (paid — fallback only)
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"

    # --- Embeddings (free, local — no API key) ---
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # --- ChromaDB (free, local) ---
    CHROMA_PERSIST_DIR: str = str(Path(__file__).resolve().parent.parent.parent / "chroma_db")
    CHROMA_COLLECTION: str = "bis_standards"

    # --- RAG ---
    RAG_TOP_K: int = 5
    RAG_CHUNK_SIZE: int = 600
    RAG_CHUNK_OVERLAP: int = 100

    # --- App ---
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    DEBUG: bool = True

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
