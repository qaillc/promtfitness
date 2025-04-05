"""
Configuration settings for the Fitness Tracker application.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Database settings
DB_NAME = "fitness_tracker.db"
DB_PATH = os.path.join(BASE_DIR, DB_NAME)

# App settings
APP_TITLE = "Fitness Tracker App"
APP_LAYOUT = "wide"

# Feature flags for enabling/disabling features
FEATURES = {
    "advanced_metrics": True,
    "allow_data_export": True,
    "enable_gamification": False,
}
