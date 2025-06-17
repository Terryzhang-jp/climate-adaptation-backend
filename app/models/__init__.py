"""
Data models for Climate Adaptation Simulation API.
"""
from .request import (
    DecisionVar,
    CurrentValues,
    SimulationRequest,
    CompareRequest
)
from .response import (
    BlockRaw,
    SimulationResponse,
    CompareResponse,
    RankingResponse,
    HealthResponse,
    ErrorResponse
)
from .simulation import (
    SimulationMode,
    ClimateScenario,
    SimulationYear,
    SimulationParameters,
    AdaptationStrategy,
    IndicatorBenchmark
)

__all__ = [
    # Request models
    "DecisionVar",
    "CurrentValues",
    "SimulationRequest",
    "CompareRequest",

    # Response models
    "BlockRaw",
    "SimulationResponse",
    "CompareResponse",
    "RankingResponse",
    "HealthResponse",
    "ErrorResponse",

    # Simulation models
    "SimulationMode",
    "ClimateScenario",
    "SimulationYear",
    "SimulationParameters",
    "AdaptationStrategy",
    "IndicatorBenchmark"
]