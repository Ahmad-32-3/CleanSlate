"""
Configuration file for News Data Pipeline
Contains API keys, URLs, and default settings
"""
import os

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError(
        "API_KEY not found. Please create a .env file with your API key:\n"
        "API_KEY=your_api_key_here"
    )

DEFAULT_LANGUAGE = "en"
DEFAULT_FULL_CONTENT = None

RAW_DATA_DIR = "data/raw"
CLEANED_DATA_DIR = "data/cleaned"
OUTPUT_DATA_DIR = "data/output"

NORMALIZE_NUMBERS = False
MIN_ARTICLE_LENGTH = 50
MAX_ARTICLE_LENGTH = 100000

EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"

DEFAULT_OUTPUT_FORMAT = "parquet"

