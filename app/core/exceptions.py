"""
Custom exceptions for Climate Adaptation Simulation.
"""
from fastapi import HTTPException


class SimulationError(Exception):
    """Base exception for simulation errors."""
    pass


class InvalidSimulationModeError(SimulationError):
    """Raised when an invalid simulation mode is provided."""
    pass


class ScenarioNotFoundError(SimulationError):
    """Raised when a requested scenario is not found."""
    pass


class DataProcessingError(SimulationError):
    """Raised when data processing fails."""
    pass


class ConfigurationError(SimulationError):
    """Raised when configuration is invalid."""
    pass


# HTTP Exception helpers
def simulation_http_exception(detail: str, status_code: int = 500) -> HTTPException:
    """Create HTTP exception for simulation errors."""
    return HTTPException(status_code=status_code, detail=detail)


def not_found_exception(detail: str) -> HTTPException:
    """Create 404 HTTP exception."""
    return HTTPException(status_code=404, detail=detail)


def bad_request_exception(detail: str) -> HTTPException:
    """Create 400 HTTP exception."""
    return HTTPException(status_code=400, detail=detail)


def internal_server_exception(detail: str) -> HTTPException:
    """Create 500 HTTP exception."""
    return HTTPException(status_code=500, detail=detail)
