"""
API v1 routes for Climate Adaptation Simulation.
"""
from fastapi import APIRouter
from . import simulation, ranking, health

api_router = APIRouter()

# Include all route modules
api_router.include_router(health.router, tags=["health"])
api_router.include_router(simulation.router, tags=["simulation"])
api_router.include_router(ranking.router, tags=["ranking"])

__all__ = ["api_router"]