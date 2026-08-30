"""BIS Mitra — FastAPI backend for AI-Powered Indian Standards Assistant."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import chat, standards, labs

settings = get_settings()

app = FastAPI(
    title="BIS Mitra API",
    description="AI-powered assistant for Indian Standards and BIS services",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(chat.router)
app.include_router(standards.router)
app.include_router(labs.router)

@app.get("/debug-cors")
async def debug_cors():
    return {
        "cors_origins": settings.CORS_ORIGINS,
        "provider": settings.LLM_PROVIDER,
        "store": settings.GEMINI_FILE_SEARCH_STORE,
    }

@app.get("/")
async def root():
    return {
        "name": "BIS Mitra API",
        "version": "1.0.0",
        "description": "AI-powered assistant for Indian Standards and BIS services",
        "endpoints": {
            "chat": "POST /api/chat",
            "recommend": "POST /api/standards/recommend",
            "labs": "GET /api/labs?category=...&city=...",
            "health": "GET /health",
        },
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
