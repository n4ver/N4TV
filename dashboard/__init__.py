"""Flask application factory and configuration."""
import os
from flask import Flask

from .logging_config import configure_logging


def create_app() -> Flask:
    """Create and configure the Flask application.
    
    Returns:
        Configured Flask application instance.
    """
    # Initialize logging
    configure_logging()
    
    # Get the absolute path to the dashboard directory
    dashboard_dir = os.path.dirname(os.path.abspath(__file__))
    
    app = Flask(
        __name__,
        instance_relative_config=False,
        template_folder=os.path.join(dashboard_dir, 'Templates'),
        static_folder=os.path.join(dashboard_dir, 'static')
    )

    # Use environment variable for debug mode, default to False in production
    app.debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    with app.app_context():
        from . import routes  # noqa: F401

        return app