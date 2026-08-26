"""Product → Standard recommendation matcher.

Two-layer approach:
1. Semantic search against product_standards_map entries
2. Keyword extraction + rule matching for precision
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from functools import lru_cache

from app.config import get_settings
from app.services.embeddings import embed_texts, embed_query
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
    """Fallback data when CSV is not yet available — covers common categories."""
    return [
        {"product_category": "electrical appliances", "keywords": "electrical,appliance,power,electric,household,plug,socket,wire,cable", "is_number": "IS 302", "title": "Safety of household and similar electrical appliances", "description": "General safety requirements for household electrical appliances"},
        {"product_category": "electrical appliances", "keywords": "washing machine,refrigerator,air conditioner,compressor,motor", "is_number": "IS 302 Part 2", "title": "Particular requirements for specific appliances", "description": "Specific safety requirements for particular appliance types"},
        {"product_category": "packaged water", "keywords": "water,drinking,bottle,packaged,mineral,drinking water", "is_number": "IS 14543", "title": "Packaged drinking water", "description": "Requirements for packaged drinking water"},
        {"product_category": "packaged food", "keywords": "food,packaged,edible,oil,milk,spice,flour,rice,pulse", "is_number": "IS 1165", "title": "Application of the terms mark and name on processed foods", "description": "Labelling requirements for processed food products"},
        {"product_category": "food products", "keywords": "food,fssai,labelling,packaging,nutrition,ingredient", "is_number": "IS 15757", "title": "General requirements for pre-packaged foods", "description": "General labelling and packaging requirements for pre-packaged foods"},
        {"product_category": "toys", "keywords": "toys,children,kids,play,doll,game,building,blocks", "is_number": "IS 9873", "title": "Safety of toys", "description": "Safety requirements for toys — mechanical, physical, flammability, chemical"},
        {"product_category": "toys", "keywords": "toy safety,children product,infant,teether,educational toy", "is_number": "IS 15644", "title": "Safety of toys — radar toys", "description": "Additional safety requirements for radar-type toys"},
        {"product_category": "textiles", "keywords": "textile,fabric,cloth,cotton,synthetic,garment,shirt, pants,dress", "is_number": "IS 1966", "title": "Fastness of dyed and printed textiles", "description": "Colour fastness requirements for textiles"},
        {"product_category": "textiles", "keywords": "cotton,textile,label,wash care,marking,garment,apparel", "is_number": "IS 14878", "title": "General requirements for labelling of textiles", "description": "Labelling and care instructions for textile products"},
        {"product_category": "steel", "keywords": "steel,iron,metal,rod,bar,tube,pipe,sheet", "is_number": "IS 2062", "title": "Steel for general structural purposes", "description": "Chemical and mechanical requirements for structural steel"},
        {"product_category": "cement", "keywords": "cement,concrete,building,construction,OPC,PPC", "is_number": "IS 455", "title": "Portland slag cement", "description": "Specification for Portland slag cement"},
        {"product_category": "cement", "keywords": "cement,OPC,ordinary,Portland,building material", "is_number": "IS 269", "title": "Ordinary Portland cement", "description": "Specification for 33 grade ordinary Portland cement"},
        {"product_category": "plastics", "keywords": "plastic,polymer,bottle,container,packaging,HDPE,LDPE,PET,pipe", "is_number": "IS 10146", "title": "Polyethylene moulding and extrusion materials", "description": "Requirements for polyethylene materials used in moulding and extrusion"},
        {"product_category": "plastics", "keywords": "plastic pipe,water pipe,PVC,fitting,plumbing", "is_number": "IS 4985", "title": "PVC pipes for potable water supply", "description": "Specification for unplasticized PVC pipes for drinking water"},
        {"product_category": "gold jewelry", "keywords": "gold,jewelry,jewellery,ring,necklace,bangle,bracelet,hallmark", "is_number": "IS 1417", "title": "Gold jewelry — determination of purity", "description": "Quality standards for gold jewelry including hallmarking requirements"},
        {"product_category": "gold jewelry", "keywords": "hallmark,huid,gold purity,carat,karat,22k,18k,14k", "is_number": "IS 1418", "title": "Silver jewelry — determination of purity", "description": "Quality standards for silver jewelry"},
        {"product_category": "batteries", "keywords": "battery,cell,accumulator,rechargeable,dry cell,lead acid", "is_number": "IS 8144", "title": "Lead-acid starter batteries", "description": "Requirements for lead-acid batteries for automotive use"},
        {"product_category": "solar panels", "keywords": "solar,panel,photovoltaic,PV,renewable,energy module", "is_number": "IS 14286", "title": "Terrestrial photovoltaic (PV) modules", "description": "Design qualification and type approval for solar PV modules"},
        {"product_category": "LPG", "keywords": "LPG,gas,cooking gas,cylinder,stove,burner", "is_number": "IS 3156", "title": "LPG burners for domestic cooking", "description": "Safety requirements for LPG domestic cooking burners"},
        {"product_category": "helmets", "keywords": "helmet,safety helmet,bike helmet,motorcycle,riding", "is_number": "IS 4151", "title": "Protective helmets for two-wheeler riders", "description": "Safety requirements and test methods for motorcycle helmets"},
    ]


def _keyword_match_score(query: str, keywords: str) -> float:
    """Simple keyword overlap scoring."""
    query_words = set(query.lower().split())
    keyword_words = set(k.lower().strip() for k in keywords.split(","))
    overlap = query_words & keyword_words
    if not keyword_words:
        return 0.0
    return len(overlap) / len(keyword_words)


def recommend_standards(product_description: str, top_k: int = 5) -> list[StandardRecommendation]:
    """Recommend applicable IS standards based on product description."""
    product_map = _load_product_map()
    if not product_map:
        return []

    # Layer 1: Semantic search
    category_texts = [f"{row['product_category']}: {row['title']} — {row['description']}" for row in product_map]
    try:
        all_embeddings = embed_texts(category_texts + [product_description])
        query_emb = all_embeddings[-1]
        category_embs = all_embeddings[:-1]

        # Cosine similarity (embeddings are normalized by sentence-transformers)
        import numpy as np
        query_np = np.array(query_emb)
        sims = [float(np.dot(query_np, np.array(ce))) for ce in category_embs]
    except Exception:
        # Fallback if numpy/embeddings fail
        sims = [0.0] * len(product_map)

    # Layer 2: Keyword matching boost
    results = []
    for i, row in enumerate(product_map):
        keyword_score = _keyword_match_score(product_description, row.get("keywords", ""))
        combined_score = 0.6 * sims[i] + 0.4 * keyword_score

        if combined_score > 0.15:  # threshold
            results.append(StandardRecommendation(
                is_number=row["is_number"],
                title=row["title"],
                relevance_score=round(combined_score, 3),
                explanation=f"Matched for category: {row['product_category']}. {row['description']}",
            ))

    # Sort by score, deduplicate by IS number
    results.sort(key=lambda x: x.relevance_score, reverse=True)
    seen = set()
    unique = []
    for r in results:
        if r.is_number not in seen:
            seen.add(r.is_number)
            unique.append(r)

    return unique[:top_k]
