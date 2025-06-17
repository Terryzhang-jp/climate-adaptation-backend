"""
Logging configuration for Climate Adaptation Simulation.
"""
import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Setup application logging.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
        format_string: Custom format string for log messages
    
    Returns:
        Configured logger instance
    """
    if format_string is None:
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(filename)s:%(lineno)d - %(message)s"
        )
    
    # Create formatter
    formatter = logging.Formatter(format_string)
    
    # Get root logger
    logger = logging.getLogger("climate_adaptation")
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Logger instance
    """
    return logging.getLogger(f"climate_adaptation.{name}")


# Default logger setup
default_logger = setup_logging()


class LoggerMixin:
    """
    Mixin class to add logging capabilities to any class.
    """
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class."""
        return get_logger(self.__class__.__name__)


def log_simulation_start(scenario_name: str, mode: str, user_name: str) -> None:
    """Log simulation start."""
    logger = get_logger("simulation")
    logger.info(f"Starting simulation - Scenario: {scenario_name}, Mode: {mode}, User: {user_name}")


def log_simulation_end(scenario_name: str, mode: str, success: bool, duration: float = None) -> None:
    """Log simulation end."""
    logger = get_logger("simulation")
    status = "SUCCESS" if success else "FAILED"
    duration_str = f" (Duration: {duration:.2f}s)" if duration else ""
    logger.info(f"Simulation {status} - Scenario: {scenario_name}, Mode: {mode}{duration_str}")


def log_api_request(endpoint: str, method: str, user_agent: str = None) -> None:
    """Log API request."""
    logger = get_logger("api")
    user_agent_str = f" - User-Agent: {user_agent}" if user_agent else ""
    logger.info(f"API Request - {method} {endpoint}{user_agent_str}")


def log_error(error: Exception, context: str = None) -> None:
    """Log error with context."""
    logger = get_logger("error")
    context_str = f" - Context: {context}" if context else ""
    logger.error(f"Error occurred: {str(error)}{context_str}", exc_info=True)
