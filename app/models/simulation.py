"""
Simulation-specific models and data structures.
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from enum import Enum


class SimulationMode(str, Enum):
    """Enumeration of available simulation modes."""
    MONTE_CARLO = "Monte Carlo Simulation Mode"
    SEQUENTIAL = "Sequential Decision-Making Mode"
    PREDICT = "Predict Simulation Mode"
    RECORD = "Record Results Mode"


class ClimateScenario(float, Enum):
    """RCP climate scenarios."""
    RCP19 = 1.9
    RCP26 = 2.6
    RCP45 = 4.5
    RCP60 = 6.0
    RCP85 = 8.5


class SimulationYear(BaseModel):
    """Single year simulation result."""
    year: int = Field(..., description="Simulation year")
    temperature: float = Field(..., description="Temperature (°C)")
    precipitation: float = Field(..., description="Precipitation (mm)")
    available_water: float = Field(..., description="Available water")
    crop_yield: float = Field(..., description="Crop yield")
    flood_damage: float = Field(..., description="Flood damage")
    ecosystem_level: float = Field(..., description="Ecosystem level")
    municipal_cost: float = Field(..., description="Municipal cost")
    resident_burden: float = Field(..., description="Resident burden")
    forest_area: float = Field(..., description="Forest area")
    urban_level: float = Field(..., description="Urban livability level")


class SimulationParameters(BaseModel):
    """Complete set of simulation parameters."""
    start_year: int
    end_year: int
    total_years: int
    base_temp: float
    temp_trend: float
    temp_uncertainty: float
    base_precip: float
    precip_trend: float
    base_precip_uncertainty: float
    # ... (can be extended with all parameters from config)


class AdaptationStrategy(BaseModel):
    """Represents a complete adaptation strategy."""
    name: str = Field(..., description="Strategy name")
    description: Optional[str] = Field(None, description="Strategy description")
    planting_trees_amount: float = Field(0.0, description="Tree planting amount")
    house_migration_amount: float = Field(0.0, description="House migration amount")
    dam_levee_construction_cost: float = Field(0.0, description="Dam/levee construction cost")
    paddy_dam_construction_cost: float = Field(0.0, description="Paddy dam construction cost")
    capacity_building_cost: float = Field(0.0, description="Capacity building cost")
    transportation_invest: float = Field(0.0, description="Transportation investment")
    agricultural_RnD_cost: float = Field(0.0, description="Agricultural R&D cost")


class IndicatorBenchmark(BaseModel):
    """Benchmark values for normalizing indicators."""
    best: float = Field(..., description="Best possible value")
    worst: float = Field(..., description="Worst possible value")
    invert: bool = Field(False, description="Whether lower values are better")
