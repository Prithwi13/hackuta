import os
from dotenv import load_dotenv

load_dotenv()

# API keys are loaded from the local environment. Never commit a real key.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# File paths
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
STATIC_FOLDER = 'static'

# Video settings
DEFAULT_VIDEO_DURATION = 3  # seconds per photo
DEFAULT_TRANSITION_DURATION = 0.5  # seconds
DEFAULT_VIDEO_WIDTH = 1920
DEFAULT_VIDEO_HEIGHT = 1080


