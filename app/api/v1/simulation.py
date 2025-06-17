"""
Simulation API routes for Climate Adaptation Simulation.
Maintains exact compatibility with original main.py endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends
import pandas as pd
import numpy as np
from typing import Dict, Any

from ...models import SimulationRequest, SimulationResponse, CompareRequest, CompareResponse
from ...services import SimulationService, DataService
from ...config import DEFAULT_PARAMS, rcp_climate_params
from ...utils import (
    process_simulation_request, validate_simulation_mode, 
    format_simulation_response, aggregate_blocks
)

router = APIRouter()

# Service instances (in production, these would be dependency injected)
simulation_service = SimulationService()
data_service = DataService()


@router.post("/simulate", response_model=SimulationResponse)
async def run_simulation(req: SimulationRequest):
    """
    Run climate adaptation simulation.
    EXACT COPY of original main.py /simulate endpoint logic.
    """
    scenario_name = req.scenario_name
    mode = req.mode
    
    # Validate mode
    if not validate_simulation_mode(mode):
        raise HTTPException(status_code=400, detail=f"Unknown mode: {mode}")
    
    # Process request data
    request_data = process_simulation_request(req.model_dump())
    
    # Update params based on RCP scenario
    rcp_param = {}
    if req.decision_vars:
        rcp_param = rcp_climate_params.get(req.decision_vars[0].cp_climate_params, {})
    request_data['rcp_params'] = rcp_param
    
    all_df = pd.DataFrame()
    block_scores = []
    
    try:
        if mode == "Monte Carlo Simulation Mode":
            # Monte Carlo simulation
            result = simulation_service.run_monte_carlo_simulation(request_data)
            all_df = pd.DataFrame(result['data'])
            block_scores = result['block_scores']
            
        elif mode == "Sequential Decision-Making Mode":
            # Sequential decision-making simulation
            result = simulation_service.run_sequential_simulation(request_data)
            all_df = result['dataframe']
            block_scores = aggregate_blocks(all_df)
            
            # Save results (exact logic from original)
            data_service.save_sequential_results(
                req.user_name, scenario_name, 
                [dv.model_dump() for dv in req.decision_vars], 
                block_scores
            )
            
        elif mode == "Predict Simulation Mode":
            # Prediction simulation
            result = simulation_service.run_prediction_simulation(request_data)
            all_df = pd.DataFrame(result['data'])
            block_scores = result['block_scores']
            
        elif mode == "Record Results Mode":
            # Record results to frontend
            success = data_service.record_results_to_frontend()
            if not success:
                raise HTTPException(status_code=500, detail="Failed to record results")
            
            return SimulationResponse(
                scenario_name=scenario_name,
                data=[],
                block_scores=[]
            )
        
        # Store scenario data for comparison (except for Predict mode)
        if mode != "Predict Simulation Mode":
            data_service.store_scenario_data(scenario_name, all_df.to_dict(orient="records"))
        
        return SimulationResponse(
            scenario_name=scenario_name,
            data=all_df.to_dict(orient="records"),
            block_scores=block_scores
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")


@router.post("/compare", response_model=CompareResponse)
async def compare_scenarios(req: CompareRequest):
    """
    Compare multiple scenarios.
    EXACT COPY of original main.py /compare endpoint logic.
    """
    try:
        result = data_service.compare_scenarios(req.scenario_names, req.variables)
        return CompareResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")


@router.get("/scenarios")
async def list_scenarios():
    """
    List all stored scenarios.
    EXACT COPY of original main.py /scenarios endpoint logic.
    """
    return {"scenarios": data_service.list_scenarios()}


@router.get("/export/{scenario_name}")
async def export_scenario_data(scenario_name: str):
    """
    Export scenario data as CSV.
    EXACT COPY of original main.py /export/{scenario_name} endpoint logic.
    """
    try:
        csv_data = data_service.export_scenario(scenario_name)
        return csv_data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")
