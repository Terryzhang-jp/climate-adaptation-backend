"""
Calculation utilities for Climate Adaptation Simulation.
Pure backend functions without any UI dependencies.
Maintains exact compatibility with original utils.py logic.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any


# Benchmark values for indicators (exact copy from original utils.py)
BENCHMARK = {
    '収量':     dict(best=10_000, worst=0,     invert=False),
    '洪水被害': dict(best=0,       worst=200_000_000, invert=True),
    '生態系':   dict(best=100,     worst=0,     invert=False),
    '都市利便性':dict(best=100,     worst=0,     invert=False),
    '予算':     dict(best=0, worst=1_000_000_000, invert=True),
    '森林面積':dict(best=10_000,     worst=0,     invert=False),
    '住民負担':dict(best=0, worst=100_000, invert=True),
}

# Time blocks for scoring (exact copy from original utils.py)
BLOCKS = [
    (2026, 2050, '2026-2050'),
    (2051, 2075, '2051-2075'),
    (2076, 2100, '2076-2100')
]


def calculate_scenario_indicators(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate scenario indicators from simulation data.
    EXACT COPY of original calculate_scenario_indicators function.
    """
    last_ecosystem = df.loc[df['Year'] == 2100, 'Ecosystem Level']
    ecosystem_level_end = last_ecosystem.values[0] if not last_ecosystem.empty else float('nan')
    return {
        '収量': df['Crop Yield'].sum(),
        '洪水被害': df['Flood Damage'].sum(),
        '生態系': ecosystem_level_end,
        '森林面積': df['Forest Area'].mean(),
        '予算': df['Municipal Cost'].sum(),
        '住民負担': df['Resident Burden'].sum(),
        '都市利便性': df['Urban Level'].mean(),
    }


def aggregate_blocks(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Aggregate simulation results into time blocks with scoring.
    EXACT COPY of original aggregate_blocks function.
    """
    records = []
    for s, e, label in BLOCKS:
        mask = (df['Year'] >= s) & (df['Year'] <= e)
        if df.loc[mask].empty:
            continue
        raw = _raw_values(df, s, e)
        score = {k: _scale_to_100(v, k) for k, v in raw.items()}
        total = float(np.mean(list(score.values())))
        records.append(dict(period=label, raw=raw, score=score, total_score=total))
    return records


def _scale_to_100(raw_val: float, metric: str) -> float:
    """
    Scale raw value to 0-100 score based on benchmark.
    EXACT COPY of original _scale_to_100 function.
    """
    b = BENCHMARK[metric]
    v = np.clip(raw_val, b['worst'], b['best']) if b['worst'] < b['best'] else np.clip(raw_val, b['best'], b['worst'])
    if b['invert']:
        score = 100 * (b['worst'] - v) / (b['worst'] - b['best'])
    else:
        score = 100 * (v - b['worst']) / (b['best'] - b['worst'])
    return float(np.round(score, 1))


def _raw_values(df: pd.DataFrame, start: int, end: int) -> Dict[str, float]:
    """
    Extract raw values for a time period.
    EXACT COPY of original _raw_values function.
    """
    mask = (df['Year'] >= start) & (df['Year'] <= end)
    return {
        '収量': df.loc[mask, 'Crop Yield'].sum(),
        '洪水被害': df.loc[mask, 'Flood Damage'].sum(),
        '予算': df.loc[mask, 'Municipal Cost'].sum(),
        '住民負担': df.loc[mask, 'Resident Burden'].sum(),
        '生態系': df.loc[mask, 'Ecosystem Level'].mean(),
        '森林面積': df.loc[mask, 'Forest Area'].mean(),
        '都市利便性': df.loc[mask, 'Urban Level'].mean(),
    }


def create_line_chart_data(df: pd.DataFrame, x_column: str, y_column: str, 
                          group_column: str = None, title: str = '', 
                          x_title: str = '', y_title: str = '') -> Dict[str, Any]:
    """
    Create line chart data structure (without rendering).
    Modified from original to return data instead of rendering with streamlit.
    """
    chart_data = {
        'title': title,
        'x_title': x_title,
        'y_title': y_title,
        'x_data': df[x_column].tolist(),
        'y_data': df[y_column].tolist(),
        'series': []
    }
    
    if group_column:
        groups = df[group_column].unique()
        for group in groups:
            df_group = df[df[group_column] == group]
            chart_data['series'].append({
                'name': str(group),
                'x_data': df_group[x_column].tolist(),
                'y_data': df_group[y_column].tolist()
            })
    else:
        chart_data['series'].append({
            'name': y_column,
            'x_data': df[x_column].tolist(),
            'y_data': df[y_column].tolist()
        })
    
    return chart_data


def create_scatter_plot_data(data: pd.DataFrame, x_axis: str, y_axis: str, 
                           scenario_column: str = 'Scenario', title: str = '') -> Dict[str, Any]:
    """
    Create scatter plot data structure (without rendering).
    Modified from original to return data instead of rendering with streamlit.
    """
    chart_data = {
        'title': title,
        'x_title': x_axis,
        'y_title': y_axis,
        'series': []
    }
    
    for scenario in data[scenario_column].unique():
        df_scenario = data[data[scenario_column] == scenario]
        chart_data['series'].append({
            'name': scenario,
            'x_data': df_scenario[x_axis].tolist(),
            'y_data': df_scenario[y_axis].tolist()
        })
    
    return chart_data


def compare_scenarios_data(scenarios_data: Dict[str, pd.DataFrame], 
                          variables: List[str]) -> Dict[str, Any]:
    """
    Compare scenarios and return comparison data.
    Modified from original to return data instead of using streamlit UI.
    """
    if not scenarios_data:
        return {'error': 'No scenarios provided for comparison'}
    
    indicators_result = {}
    for name, df in scenarios_data.items():
        indicators_result[name] = calculate_scenario_indicators(df)
    
    return {
        'message': 'Comparison results',
        'comparison': indicators_result,
        'variables': variables
    }
