"""
Data processing utilities for Climate Adaptation Simulation.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional
import shutil
import glob


def save_ranking_data(df: pd.DataFrame, file_path: Path, user_name: str, 
                     scenario_name: str, block_scores: List[Dict]) -> None:
    """
    Save ranking data to file.
    Maintains exact logic from original main.py.
    """
    df_csv = pd.DataFrame(block_scores)
    df_csv['user_name'] = user_name
    df_csv['scenario_name'] = scenario_name
    df_csv['timestamp'] = pd.Timestamp.utcnow()
    
    if file_path.exists():
        old = pd.read_csv(file_path, sep='\t')
        merged = (
            old.set_index(['user_name', 'scenario_name', 'period'])
            .combine_first(df_csv.set_index(['user_name', 'scenario_name', 'period']))
            .reset_index()
        )
        merged.to_csv(file_path, sep='\t', index=False)
    else:
        df_csv.to_csv(file_path, sep='\t', index=False)


def save_action_log(decision_vars: List[Dict], user_name: str, 
                   scenario_name: str, file_path: Path) -> None:
    """
    Save action log data to file.
    Maintains exact logic from original main.py.
    """
    df_log = pd.DataFrame(decision_vars)
    df_log['user_name'] = user_name
    df_log['scenario_name'] = scenario_name
    df_log['timestamp'] = pd.Timestamp.utcnow()
    
    if file_path.exists():
        df_old = pd.read_csv(file_path)
        df_combined = pd.concat([df_old, df_log], ignore_index=True)
    else:
        df_combined = df_log
    
    df_combined.to_csv(file_path, index=False)


def save_user_name(user_name: str, file_path: Path) -> None:
    """
    Save user name to file.
    Maintains exact logic from original main.py.
    """
    pd.Series([user_name]).to_csv(file_path, index=False)


def load_ranking_data(file_path: Path) -> List[Dict[str, Any]]:
    """
    Load and process ranking data.
    Maintains exact logic from original main.py.
    """
    if not file_path.exists():
        return []
    
    try:
        df = pd.read_csv(file_path, sep='\t')
        latest = df.sort_values('timestamp').drop_duplicates(
            ['user_name', 'scenario_name', 'period'], keep='last'
        )
        rank_df = (
            latest.groupby('user_name')['total_score']
            .mean()
            .reset_index()
            .sort_values('total_score', ascending=False)
            .reset_index(drop=True)
        )
        rank_df['rank'] = rank_df.index + 1
        return rank_df.to_dict(orient='records')
    except Exception as e:
        print(f"Error loading ranking data: {e}")
        return []


def load_block_scores(file_path: Path) -> List[Dict[str, Any]]:
    """
    Load block scores data.
    Maintains exact logic from original main.py.
    """
    if not file_path.exists():
        return []
    
    try:
        df = pd.read_csv(file_path, sep="\t")
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error loading block scores: {e}")
        return []


def copy_results_to_frontend(src_dir: Path, dst_dir: Path) -> bool:
    """
    Copy result files to frontend directory.
    Maintains exact logic from original main.py Record Results Mode.
    """
    try:
        dst_dir.mkdir(parents=True, exist_ok=True)
        
        for filepath in glob.glob(str(src_dir / "*.csv")) + glob.glob(str(src_dir / "*.tsv")):
            shutil.copy(filepath, dst_dir)
        
        return True
    except Exception as e:
        print(f"Error copying results to frontend: {e}")
        return False


def export_scenario_csv(data: pd.DataFrame) -> str:
    """
    Export scenario data as CSV string.
    """
    return data.to_csv(index=False)


def process_simulation_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process and validate simulation request data.
    """
    # Extract and validate decision variables
    decision_vars = []
    if 'decision_vars' in request_data and request_data['decision_vars']:
        for dv in request_data['decision_vars']:
            if isinstance(dv, dict):
                decision_vars.append(dv)
            else:
                # Handle Pydantic model objects
                decision_vars.append(dv.model_dump() if hasattr(dv, 'model_dump') else dv.__dict__)
    
    # Extract current values
    current_values = request_data.get('current_year_index_seq', {})
    if hasattr(current_values, 'model_dump'):
        current_values = current_values.model_dump()
    elif not isinstance(current_values, dict):
        current_values = current_values.__dict__
    
    return {
        'user_name': request_data.get('user_name', ''),
        'scenario_name': request_data.get('scenario_name', ''),
        'mode': request_data.get('mode', ''),
        'decision_vars': decision_vars,
        'num_simulations': request_data.get('num_simulations', 100),
        'initial_values': current_values,
        'year': decision_vars[0]['year'] if decision_vars and len(decision_vars) > 0 else 2026
    }


def validate_simulation_mode(mode: str) -> bool:
    """
    Validate simulation mode.
    """
    valid_modes = [
        "Monte Carlo Simulation Mode",
        "Sequential Decision-Making Mode", 
        "Predict Simulation Mode",
        "Record Results Mode"
    ]
    return mode in valid_modes


def format_simulation_response(scenario_name: str, data: List[Dict], 
                             block_scores: List[Dict] = None) -> Dict[str, Any]:
    """
    Format simulation response data.
    """
    return {
        'scenario_name': scenario_name,
        'data': data,
        'block_scores': block_scores or []
    }
