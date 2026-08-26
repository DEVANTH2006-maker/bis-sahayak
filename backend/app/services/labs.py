"""Lab lookup service — searchable BIS-recognized testing laboratory directory."""

from __future__ import annotations

import json
from pathlib import Path
from functools import lru_cache

from app.models.schemas import Lab

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
LABS_FILE = DATA_DIR / "labs.json"


@lru_cache
def _load_labs() -> list[dict]:
    """Load lab data from JSON file."""
    if not LABS_FILE.exists():
        return _get_fallback_labs()

    with open(LABS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_fallback_labs() -> list[dict]:
    """Fallback data when labs.json is not yet available."""
    return [
        {"name": "National Test House (NTH)", "address": "136, G.S. Road, Guwahati", "city": "Guwahati", "state": "Assam", "phone": "+91-361-2334949", "email": "nthguwahati@gov.in", "categories": ["electrical", "textiles", "steel", "cement", "plastics"], "accreditation": "NABL"},
        {"name": "Bureau of Indian Standards — Regional Laboratory (Delhi)", "address": "9Bahadur Shah Zafar Marg, New Delhi", "city": "New Delhi", "state": "Delhi", "phone": "+91-11-23370124", "email": "", "categories": ["electrical", "electronic", "food", "toys", "textiles"], "accreditation": "NABL, BIS"},
        {"name": "Central电力 Research Institute (CPRI)", "address": "12, Thimmaiah Road, Bangalore", "city": "Bangalore", "state": "Karnataka", "phone": "+91-80-22249661", "email": "", "categories": ["electrical", "power", "transformers", "cables"], "accreditation": "NABL, BIS"},
        {"name": "Electronics Regional Test Laboratory (ERTL)", "address": "38, Nelson Manickam Road, Chennai", "city": "Chennai", "state": "Tamil Nadu", "phone": "+91-44-23741191", "email": "", "categories": ["electronic", "IT equipment", "telecom"], "accreditation": "NABL, BIS"},
        {"name": "Central Institute of Plastics Engineering & Technology (CIPET)", "address": "T.V.K. Industrial Estate, Guindy, Chennai", "city": "Chennai", "state": "Tamil Nadu", "phone": "+91-44-22254631", "email": "", "categories": ["plastics", "polymer", "packaging"], "accreditation": "NABL"},
        {"name": "National Metallurgical Laboratory (NML)", "address": "Jamshedpur, Jharkhand", "city": "Jamshedpur", "state": "Jharkhand", "phone": "+91-657-2345085", "email": "", "categories": ["metals", "steel", "alloys"], "accreditation": "NABL"},
        {"name": "Shriram Institute for Industrial Research", "address": "14, Satsang Vihar Marg, New Delhi", "city": "New Delhi", "state": "Delhi", "phone": "+91-11-26341707", "email": "", "categories": ["chemicals", "rubber", "plastics", "textiles"], "accreditation": "NABL"},
        {"name": "BIS Laboratory, Kolkata", "address": "5, Middleton Street, Kolkata", "city": "Kolkata", "state": "West Bengal", "phone": "+91-33-22487427", "email": "", "categories": ["food", "textiles", "chemicals", "building materials"], "accreditation": "BIS"},
        {"name": "Indian Oil Corporation R&D Centre", "address": "Sector-13, Faridabad", "city": "Faridabad", "state": "Haryana", "phone": "+91-129-2272810", "email": "", "categories": ["petroleum", "lubricants", "fuels"], "accreditation": "NABL"},
        {"name": "National Sugar Institute", "address": "Kanpur, Uttar Pradesh", "city": "Kanpur", "state": "Uttar Pradesh", "phone": "+91-512-2530331", "email": "", "categories": ["food", "sugar", "confectionery"], "accreditation": "NABL"},
        {"name": "BIS Regional Lab Mumbai", "address": "BIS House, 501, NDVI, Plot C-4, Bandra Kurla Complex, Mumbai", "city": "Mumbai", "state": "Maharashtra", "phone": "+91-22-26590215", "email": "", "categories": ["electrical", "food", "toys", "textiles", "metals"], "accreditation": "NABL, BIS"},
        {"name": "Central Leather Research Institute (CLRI)", "address": "Adyar, Chennai", "city": "Chennai", "state": "Tamil Nadu", "phone": "+91-44-24411070", "email": "", "categories": ["leather", "footwear", "textiles"], "accreditation": "NABL"},
    ]


def search_labs(category: str = "", city: str = "", state: str = "") -> list[Lab]:
    """Search labs by category, city, or state."""
    all_labs = _load_labs()

    results = []
    for lab_data in all_labs:
        # Filter by category
        if category:
            cat_lower = category.lower()
            lab_cats = [c.lower() for c in lab_data.get("categories", [])]
            if not any(cat_lower in c for c in lab_cats):
                continue

        # Filter by city
        if city and city.lower() not in lab_data.get("city", "").lower():
            continue

        # Filter by state
        if state and state.lower() not in lab_data.get("state", "").lower():
            continue

        results.append(Lab(**lab_data))

    return results


def get_all_labs() -> list[Lab]:
    """Return all labs."""
    return [Lab(**lab_data) for lab_data in _load_labs()]
