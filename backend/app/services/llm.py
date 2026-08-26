"""Unified LLM client — supports Ollama (free/local), Gemini (free tier), OpenAI, Anthropic."""

from __future__ import annotations
import httpx
from app.config import get_settings


def _ollama_complete(system_prompt: str, user_prompt: str, max_tokens: int, temperature: float) -> str:
    settings = get_settings()
    payload = {
        "model": settings.OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "options": {"temperature": temperature, "num_predict": max_tokens},
    }
    resp = httpx.post(f"{settings.OLLAMA_BASE_URL}/api/chat", json=payload, timeout=120.0)
    resp.raise_for_status()
    return resp.json()["message"]["content"]


def _gemini_complete(system_prompt: str, user_prompt: str, max_tokens: int, temperature: float) -> str:
    settings = get_settings()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": f"{system_prompt}\n\n{user_prompt}"}]}],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": temperature,
        },
        "systemInstruction": {"parts": [{"text": system_prompt}]},
    }
    resp = httpx.post(url, json=payload, timeout=60.0)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


def _openai_complete(system_prompt: str, user_prompt: str, max_tokens: int, temperature: float) -> str:
    from openai import OpenAI
    settings = get_settings()
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    resp = client.chat.completions.create(
        model=settings.OPENAI_MODEL, max_tokens=max_tokens, temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return resp.choices[0].message.content


def _anthropic_complete(system_prompt: str, user_prompt: str, max_tokens: int, temperature: float) -> str:
    import anthropic
    settings = get_settings()
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    resp = client.messages.create(
        model=settings.ANTHROPIC_MODEL, max_tokens=max_tokens, temperature=temperature,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return resp.content[0].text


def llm_complete(system_prompt: str, user_prompt: str, *, max_tokens: int = 2048, temperature: float = 0.3) -> str:
    settings = get_settings()
    provider = settings.LLM_PROVIDER.lower()
    if provider == "ollama":
        return _ollama_complete(system_prompt, user_prompt, max_tokens, temperature)
    elif provider == "gemini":
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set")
        return _gemini_complete(system_prompt, user_prompt, max_tokens, temperature)
    elif provider == "openai":
        return _openai_complete(system_prompt, user_prompt, max_tokens, temperature)
    elif provider == "anthropic":
        return _anthropic_complete(system_prompt, user_prompt, max_tokens, temperature)
    else:
        raise ValueError(f"Unknown provider: {provider}")
