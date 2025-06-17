"""
Request models for Climate Adaptation Simulation API.
Maintains exact compatibility with original models.py.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class DecisionVar(BaseModel):
    """
    Decision variables for climate adaptation strategies.
    Exact copy from original models.py.
    """
    year: int = Field(..., description="Target year for the decision")
    planting_trees_amount: float = Field(..., description="Amount of trees to plant (1000 trees = 1ha)")
    house_migration_amount: float = Field(..., description="Number of houses to migrate from risky areas")
    dam_levee_construction_cost: float = Field(..., description="Investment in dam/levee construction (100M yen units)")
    paddy_dam_construction_cost: float = Field(..., description="Investment in paddy dam construction (1M yen units)")
    capacity_building_cost: float = Field(..., description="Investment in disaster preparedness training (1M yen units)")
    transportation_invest: float = Field(..., description="Investment in transportation infrastructure (10M yen units)")
    agricultural_RnD_cost: float = Field(..., description="Investment in agricultural R&D (10M yen units)")
    cp_climate_params: float = Field(..., description="RCP climate scenario parameter (1.9, 2.6, 4.5, 6.0, 8.5)")


class CurrentValues(BaseModel):
    """
    Current state values for the simulation.
    Exact copy from original models.py.
    """
    temp: float = Field(..., description="Current temperature (°C)")
    precip: float = Field(..., description="Current precipitation (mm)")
    municipal_demand: float = Field(..., description="Municipal water demand")
    available_water: float = Field(..., description="Available water amount")
    crop_yield: float = Field(..., description="Current crop yield")
    hot_days: float = Field(..., description="Number of hot days")
    extreme_precip_freq: float = Field(..., description="Extreme precipitation frequency")
    ecosystem_level: float = Field(..., description="Ecosystem health level")
    levee_level: Optional[float] = Field(0.0, description="Current levee protection level")
    high_temp_tolerance_level: Optional[float] = Field(0.0, description="Crop heat tolerance level")
    forest_area: Optional[float] = Field(0.0, description="Current forest area (ha)")
    planting_history: Optional[Dict[int, float]] = Field(default_factory=dict, description="History of tree planting by year")
    urban_level: Optional[float] = Field(0.0, description="Urban livability level")
    resident_capacity: Optional[float] = Field(0.0, description="Resident disaster preparedness capacity")
    transportation_level: Optional[float] = Field(100.0, description="Transportation infrastructure level")
    levee_investment_total: Optional[float] = Field(0.0, description="Total accumulated levee investment")
    RnD_investment_total: Optional[float] = Field(0.0, description="Total accumulated R&D investment")
    risky_house_total: Optional[float] = Field(10000.0, description="Number of houses in risky areas")
    non_risky_house_total: Optional[float] = Field(0.0, description="Number of houses in safe areas")
    resident_burden: Optional[float] = Field(0.0, description="Financial burden on residents")
    biodiversity_level: Optional[float] = Field(0.0, description="Biodiversity level")


class SimulationRequest(BaseModel):
    """
    Request model for simulation endpoint.
    Exact copy from original models.py.
    """
    user_name: str = Field(..., description="Name of the user running the simulation")
    scenario_name: str = Field(..., description="Name of the scenario")
    mode: str = Field(..., description="Simulation mode: 'Monte Carlo Simulation Mode', 'Sequential Decision-Making Mode', 'Predict Simulation Mode', or 'Record Results Mode'")
    decision_vars: List[DecisionVar] = Field(default_factory=list, description="List of decision variables")
    num_simulations: int = Field(100, description="Number of Monte Carlo simulations to run")
    current_year_index_seq: CurrentValues = Field(..., description="Current state values for the simulation")


class CompareRequest(BaseModel):
    """
    Request model for scenario comparison.
    Exact copy from original models.py.
    """
    scenario_names: List[str] = Field(..., description="List of scenario names to compare")
    variables: List[str] = Field(..., description="List of variables to compare")
