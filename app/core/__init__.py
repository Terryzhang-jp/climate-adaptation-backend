"""
Core utilities for Climate Adaptation Simulation.
"""
from .exceptions import (
    SimulationError,
    InvalidSimulationModeError,
    ScenarioNotFoundError,
    DataProcessingError,
    ConfigurationError,
    simulation_http_exception,
    not_found_exception,
    bad_request_exception,
    internal_server_exception
)
from .logging import (
    setup_logging,
    get_logger,
    LoggerMixin,
    log_simulation_start,
    log_simulation_end,
    log_api_request,
    log_error
)

__all__ = [
    # Exceptions
    "SimulationError",
    "InvalidSimulationModeError",
    "ScenarioNotFoundError",
    "DataProcessingError",
    "ConfigurationError",
    "simulation_http_exception",
    "not_found_exception",
    "bad_request_exception",
    "internal_server_exception",

    # Logging
    "setup_logging",
    "get_logger",
    "LoggerMixin",
    "log_simulation_start",
    "log_simulation_end",
    "log_api_request",
    "log_error"
]