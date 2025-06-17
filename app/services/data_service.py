"""
Data management service for Climate Adaptation Simulation.
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional

from ..config import RANK_FILE, ACTION_LOG_FILE, YOUR_NAME_FILE, DATA_DIR
from ..utils import (
    save_ranking_data, save_action_log, save_user_name,
    load_ranking_data, load_block_scores, copy_results_to_frontend,
    export_scenario_csv, calculate_scenario_indicators
)


class DataService:
    """
    Service for managing simulation data, rankings, and file operations.
    """
    
    def __init__(self):
        self.scenarios_data: Dict[str, pd.DataFrame] = {}
    
    def save_sequential_results(self, user_name: str, scenario_name: str, 
                              decision_vars: List[Dict], block_scores: List[Dict]) -> None:
        """
        Save results from sequential decision-making mode.
        Maintains exact logic from original main.py.
        """
        # Save action log
        save_action_log(decision_vars, user_name, scenario_name, ACTION_LOG_FILE)
        
        # Save user name
        save_user_name(user_name, YOUR_NAME_FILE)
        
        # Save ranking data
        save_ranking_data(pd.DataFrame(), RANK_FILE, user_name, scenario_name, block_scores)
    
    def get_ranking(self) -> List[Dict[str, Any]]:
        """
        Get user ranking data.
        Maintains exact logic from original main.py.
        """
        return load_ranking_data(RANK_FILE)
    
    def get_block_scores(self) -> List[Dict[str, Any]]:
        """
        Get block scores data.
        Maintains exact logic from original main.py.
        """
        return load_block_scores(RANK_FILE)
    
    def compare_scenarios(self, scenario_names: List[str], variables: List[str]) -> Dict[str, Any]:
        """
        Compare multiple scenarios.
        Maintains exact logic from original main.py.
        """
        selected_data = {
            name: self.scenarios_data[name] 
            for name in scenario_names 
            if name in self.scenarios_data
        }
        
        if not selected_data:
            raise ValueError("No scenarios found for given names.")
        
        indicators_result = {
            name: calculate_scenario_indicators(df) 
            for name, df in selected_data.items()
        }
        
        return {
            'message': 'Comparison results',
            'comparison': indicators_result
        }
    
    def store_scenario_data(self, scenario_name: str, data: List[Dict]) -> None:
        """
        Store scenario data for later use.
        """
        df = pd.DataFrame(data)
        self.scenarios_data[scenario_name] = df
    
    def get_scenario_data(self, scenario_name: str) -> Optional[pd.DataFrame]:
        """
        Get stored scenario data.
        """
        return self.scenarios_data.get(scenario_name)
    
    def list_scenarios(self) -> List[str]:
        """
        List all stored scenario names.
        """
        return list(self.scenarios_data.keys())
    
    def export_scenario(self, scenario_name: str) -> str:
        """
        Export scenario data as CSV.
        """
        if scenario_name not in self.scenarios_data:
            raise ValueError(f"Scenario '{scenario_name}' not found.")
        
        return export_scenario_csv(self.scenarios_data[scenario_name])
    
    def record_results_to_frontend(self) -> bool:
        """
        Copy result files to frontend directory.
        Maintains exact logic from original main.py Record Results Mode.
        """
        src_dir = DATA_DIR
        dst_dir = Path(__file__).parent.parent.parent.parent / "frontend" / "public" / "results" / "data"
        
        return copy_results_to_frontend(src_dir, dst_dir)
