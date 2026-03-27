import os
import sys
import csv
import json
import logging
import requests
import psycopg2
import pandas as pd

from datetime import datetime, timezone, timedelta
from pathlib import Path
# from dotenv import load_dotenv

# Database Constants and Configuration

SCRIPT_DIR = Path(__file__).parent.resolve()
#load_dotenv(SCRIPT_DIR / ".env")

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", 5432)),
    "dbname":   os.getenv("DB_NAME", "earthquake_db"),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),    
}

CSV_OUTPUT_DIR = Path(os.getenv("CSV_OUTPUT_DIR", SCRIPT_DIR / "csv_exports"))
LOG_FILE       = Path(os.getenv("LOG_FILE",       SCRIPT_DIR / "logs" / "earthquake.log"))

USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

LOOKBACK_MINUTES = 10