"""Product → Standard recommendation matcher.

Uses keyword/rule matching so the backend does not need to load
the large SentenceTransformer model.
"""

from __future__ import annotations

import csv
from pathlib import Path
from functools import lru_cache

from app.models.schemas import StandardRecommendation

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
PRODUCT_MAP_FILE = DATA_DIR / "product_standards_map.csv"


@lru_cache
def _load_product_map() -> list[dict]:
    """Load the product→standard mapping from CSV."""
    if not PRODUCT_MAP_FILE.exists():
        return _get_fallback_product_map()

    rows = []
    with open(PRODUCT_MAP_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    return rows


def _get_fallback_product_map() -> list[dict]:
    """Fallback data when CSV is not available."""
    return [
        {
            "product_category": "electrical appliances",
            "keywords": "electrical,appliance,power,electric,household,plug,socket,wire,cable",
            "is_number": "IS 302",
            "title": "Safety of household and similar electrical appliances",
            "description": "General safety requirements for household electrical appliances",
        },
        {
            "product_category": "packaged water",
            "keywords": "water,drinking,bottle,packaged,mineral,drinking water",
            "is_number": "IS 14543",
            "title": "Packaged drinking water",
            "description": "Requirements for packaged drinking water",
        },
        {
            "product_category": "packaged food",
            "keywords": "food,packaged,edible,oil,milk,spice,flour,rice,pulse",
            "is_number": "IS 1165",
            "title": "Application of the terms mark and name on processed foods",
            "description": "Labelling requirements for processed food products",
        },
        {
            "product_category": "food products",
            "keywords": "food,fssai,labelling,packaging,nutrition,ingredient",
            "is_number": "IS 15757",
            "title": "General requirements for pre-packaged foods",
            "description": "General labelling and packaging requirements for pre-packaged foods",
        },
        {
            "product_category": "toys",
            "keywords": "toys,children,kids,play,doll,game,building,blocks",
            "is_number": "IS 9873",
            "title": "Safety of toys",
            "description": "Safety requirements for toys",
        },
        {
            "product_category": "textiles",
            "keywords": "textile,fabric,cloth,cotton,synthetic,garment,shirt,pants,dress",
            "is_number": "IS 1966",
            "title": "Fastness of dyed and printed textiles",
            "description": "Colour fastness requirements for textiles",
        },
        {
            "product_category": "steel",
            "keywords": "steel,iron,metal,rod,bar,tube,pipe,sheet",
            "is_number": "IS 2062",
            "title": "Steel for general structural purposes",
            "description": "Chemical and mechanical requirements for structural steel",
        },
        {
            "product_category": "cement",
            "keywords": "cement,concrete,building,construction,OPC,PPC",
            "is_number": "IS 455",
            "title": "Portland slag cement",
            "description": "Specification for Portland slag cement",
        },
        {
            "product_category": "plastics",
            "keywords": "plastic,polymer,bottle,container,packaging,HDPE,LDPE,PET,pipe",
            "is_number": "IS 10146",
            "title": "Polyethylene moulding and extrusion materials",
            "description": "Requirements for polyethylene materials",
        },
        {
            "product_category": "gold jewelry",
            "keywords": "gold,jewelry,jewellery,ring,necklace,bangle,bracelet,hallmark",
            "is_number": "IS 1417",
            "title": "Gold jewelry — determination of purity",
            "description": "Quality standards for gold jewelry",
        },
        {
            "product_category": "batteries",
            "keywords": "battery,cell,accumulator,rechargeable,dry cell,lead acid",
            "is_number": "IS 8144",
            "title": "Lead-acid starter batteries",
            "description": "Requirements for lead-acid batteries",
        },
        {
            "product_category": "solar panels",
            "keywords": "solar,panel,photovoltaic,PV,renewable,energy,module",
            "is_number": "IS 14286",
            "title": "Terrestrial photovoltaic modules",
            "description": "Requirements for solar PV modules",
        },
        {
            "product_category": "helmets",
            "keywords": "helmet,safety helmet,bike helmet,motorcycle,riding",
            "is_number": "IS 4151",
            "title": "Protective helmets for two-wheeler riders",
            "description": "Safety requirements for motorcycle helmets",
        },
    ]


def _keyword_match_score(query: str, keywords: str) -> float:
    """Calculate keyword overlap score."""
    query_words = set(query.lower().split())
    keyword_words = {
        k.lower().strip()
        for k in keywords.split(",")
    }

    if not keyword_words:
        return 0.0

    overlap = query_words & keyword_words

    return len(overlap) / len(keyword_words)


def recommend_standards(
    product_description: str,
    top_k: int = 5,
) -> list[StandardRecommendation]:
    """Recommend applicable IS standards using keyword matching."""

    product_map = _load_product_map()

    if not product_map:
        return []

    results = []

    query = product_description.lower()

    for row in product_map:
        keywords = row.get("keywords", "")

        # Keyword matching
        keyword_score = _keyword_match_score(
            product_description,
            keywords,
        )

        # Also check individual keywords directly in the query.
        direct_matches = 0
        keyword_list = [
            k.strip().lower()
            for k in keywords.split(",")
            if k.strip()
        ]

        for keyword in keyword_list:
            if keyword in query:
                direct_matches += 1

        if keyword_list:
            direct_score = direct_matches / len(keyword_list)
        else:
            direct_score = 0.0

        combined_score = max(
            keyword_score,
            direct_score,
        )

        if combined_score > 0:
            results.append(
                StandardRecommendation(
                    is_number=row["is_number"],
                    title=row["title"],
                    relevance_score=round(combined_score, 3),
                    explanation=(
                        f"Matched for category: "
                        f"{row['product_category']}. "
                        f"{row['description']}"
                    ),
                )
            )

    results.sort(
        key=lambda x: x.relevance_score,
        reverse=True,
    )

    # Deduplicate by IS number
    seen = set()
    unique = []

    for result in results:
        if result.is_number not in seen:
            seen.add(result.is_number)
            unique.append(result)

    return unique[:top_k]