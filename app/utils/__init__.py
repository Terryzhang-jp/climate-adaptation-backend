"""
Utility functions for Climate Adaptation Simulation.
"""
from .calculations import (
    calculate_scenario_indicators,
    aggregate_blocks,
    create_line_chart_data,
    create_scatter_plot_data,
    compare_scenarios_data,
    BENCHMARK,
    BLOCKS
)
from .data_processing import (
    save_ranking_data,
    save_action_log,
    save_user_name,
    load_ranking_data,
    load_block_scores,
    copy_results_to_frontend,
    export_scenario_csv,
    process_simulation_request,
    validate_simulation_mode,
    format_simulation_response
)

__all__ = [
    # Calculations
    "calculate_scenario_indicators",
    "aggregate_blocks",
    "create_line_chart_data",
    "create_scatter_plot_data",
    "compare_scenarios_data",
    "BENCHMARK",
    "BLOCKS",

    # Data processing
    "save_ranking_data",
    "save_action_log",
    "save_user_name",
    "load_ranking_data",
    "load_block_scores",
    "copy_results_to_frontend",
    "export_scenario_csv",
    "process_simulation_request",
    "validate_simulation_mode",
    "format_simulation_response"
]