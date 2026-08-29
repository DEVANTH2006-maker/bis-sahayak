"""Gemini File Search based RAG service."""

from __future__ import annotations

from google import genai
from google.genai import types

from app.config import get_settings

settings = get_settings()


def rag_query(query: str, top_k: int = 5):
    """
    Query the BIS knowledge base using Gemini File Search.

    Returns:
        tuple[str, list]: answer and sources
    """

    if not settings.GEMINI_FILE_SEARCH_STORE:
        return (
            "The BIS knowledge base is not configured.",
            [],
        )

    if not settings.GEMINI_API_KEY:
        return (
            "Gemini API key is not configured.",
            [],
        )

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=query,
        config=types.GenerateContentConfig(
            tools=[
                types.Tool(
                    file_search=types.FileSearch(
                        file_search_store_names=[
                            settings.GEMINI_FILE_SEARCH_STORE
                        ]
                    )
                )
            ]
        ),
    )

    answer = response.text or "I couldn't find relevant information."

    return answer, []
