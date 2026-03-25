"""Logging configuration for N4TV Dashboard."""
import logging
import os


def configure_logging() -> None:
    """Configure logging for the application.
    
    Sets up logging to both console and file with appropriate
    formatting and log levels based on environment.
    """
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Console output
            logging.FileHandler('app.log')  # File output
        ]
    )
    
    # Suppress verbose third-party logging
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
