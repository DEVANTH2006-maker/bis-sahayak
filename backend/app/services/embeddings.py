"""Embedding service using sentence-transformers (free, local)."""

from __future__ import annotations

from functools import lru_cache
from app.config import get_settings


@lru_cache
def _get_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(get_settings().EMBEDDING_MODEL)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Return embedding vectors for a list of texts."""
    model = _get_model()
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()


def embed_query(text: str) -> list[float]:
    """Return embedding vector for a single query string."""
    return embed_texts([text])[0]
