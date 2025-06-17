"""
Response models for Climate Adaptation Simulation API.
Maintains exact compatibility with original models.py.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any


class BlockRaw(BaseModel):
    """
    Block scoring data for time periods.
    Exact copy from original models.py.
    """
    period: str = Field(..., description="Time period (e.g., '2026-2050')")
    raw: Dict[str, float] = Field(..., description="Raw indicator values for the period")
    score: Dict[str, float] = Field(..., description="Normalized scores (0-100) for indicators")
    total_score: float = Field(..., description="Overall score for the period")


class SimulationResponse(BaseModel):
    """
    Response model for simulation endpoint.
    Exact copy from original models.py.
    """
    scenario_name: str = Field(..., description="Name of the scenario")
    data: List[Dict[str, Any]] = Field(..., description="Simulation results data")
    block_scores: List[BlockRaw] = Field(..., description="Block scoring results")


class CompareResponse(BaseModel):
    """
    Response model for scenario comparison.
    Exact copy from original models.py.
    """
    message: str = Field(..., description="Response message")
    comparison: Dict[str, Any] = Field(..., description="Comparison results")


class RankingResponse(BaseModel):
    """
    Response model for ranking endpoint.
    """
    rank: int = Field(..., description="User's rank position")
    user_name: str = Field(..., description="User name")
    total_score: float = Field(..., description="Average total score")


class HealthResponse(BaseModel):
    """
    Response model for health check endpoint.
    """
    status: str = Field(..., description="Health status")
    timestamp: str = Field(..., description="Current timestamp")
    version: str = Field("1.0.0", description="API version")


class ErrorResponse(BaseModel):
    """
    Error response model.
    """
    detail: str = Field(..., description="Error message")
    error_code: str = Field(None, description="Error code")
    timestamp: str = Field(None, description="Error timestamp")
