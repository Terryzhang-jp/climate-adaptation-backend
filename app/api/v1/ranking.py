"""
Ranking API routes for Climate Adaptation Simulation.
Maintains exact compatibility with original main.py endpoints.
"""
from fastapi import APIRouter, HTTPException
from typing import List

from ...models import RankingResponse
from ...services import DataService

router = APIRouter()

# Service instance
data_service = DataService()


@router.get("/ranking", response_model=List[RankingResponse])
async def get_ranking():
    """
    Get user ranking data.
    EXACT COPY of original main.py /ranking endpoint logic.
    """
    try:
        ranking_data = data_service.get_ranking()
        return ranking_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get ranking: {str(e)}")


@router.get("/block_scores")
async def get_block_scores():
    """
    Get block scores data.
    EXACT COPY of original main.py /block_scores endpoint logic.
    """
    try:
        block_scores = data_service.get_block_scores()
        return block_scores
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get block scores: {str(e)}")
