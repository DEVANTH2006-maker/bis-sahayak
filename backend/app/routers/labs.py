"""Lab lookup API endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.models.schemas import LabSearchResponse
from app.services.labs import search_labs

router = APIRouter(prefix="/api/labs", tags=["labs"])


@router.get("", response_model=LabSearchResponse)
async def list_labs(
    category: str = Query(default="", description="Product category filter"),
    city: str = Query(default="", description="City filter"),
    state: str = Query(default="", description="State filter"),
):
    """Search BIS-recognized testing labs by category, city, or state."""
    labs = search_labs(category=category, city=city, state=state)
    return LabSearchResponse(labs=labs, total=len(labs))


@router.get("/all", response_model=LabSearchResponse)
async def list_all_labs():
    """Return all labs."""
    from app.services.labs import get_all_labs
    labs = get_all_labs()
    return LabSearchResponse(labs=labs, total=len(labs))
