"""Multilingual translation layer — detect language, translate query/answer."""

from __future__ import annotations

from app.services.llm import llm_complete

# Languages we support (extend as needed)
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "ur": "Urdu",
}


def detect_language(text: str) -> str:
    """Detect the language of input text. Returns ISO 639-1 code."""
    # Use LLM for reliable detection across Indic scripts
    system = (
        "You are a language detector. Reply with ONLY the ISO 639-1 language code "
        "(e.g. 'en', 'hi', 'bn', 'ta', 'te', 'mr', 'gu', 'kn', 'ml', 'pa', 'ur'). "
        "No other text."
    )
    result = llm_complete(system, text, max_tokens=10, temperature=0.0).strip().lower()
    return result if result in SUPPORTED_LANGUAGES else "en"


def translate_to_english(text: str, source_lang: str) -> str:
    """Translate text from source_lang to English."""
    if source_lang == "en":
        return text
    lang_name = SUPPORTED_LANGUAGES.get(source_lang, source_lang)
    system = (
        f"Translate the following {lang_name} text to English. "
        "Output ONLY the translation, nothing else."
    )
    return llm_complete(system, text, max_tokens=2048, temperature=0.0)


def translate_from_english(text: str, target_lang: str) -> str:
    """Translate English text to the target language."""
    if target_lang == "en":
        return text
    lang_name = SUPPORTED_LANGUAGES.get(target_lang, target_lang)
    system = (
        f"Translate the following English text to {lang_name}. "
        "Output ONLY the translation, nothing else. "
        "Keep technical terms (like IS numbers, clause numbers) in English if they have no standard translation."
    )
    return llm_complete(system, text, max_tokens=2048, temperature=0.0)
