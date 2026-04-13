import sys
import os
import json
import unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# test connection to the DB
DB_AVAILABLE   = False
TABLE_HAS_DATA = False

try:
    import psycopg2
    from config import DB_CONFIG, PROCESSED_TABLE
    _conn = psycopg2.connect(**DB_CONFIG)
    _cur  = _conn.cursor()
    _cur.execute(f"SELECT COUNT(*) FROM {PROCESSED_TABLE}")
    _count = _cur.fetchone()[0]
    _conn.close()
    DB_AVAILABLE   = True
    TABLE_HAS_DATA = _count > 0
except Exception as _e:
    print(f"[integration] DB not available: {_e} — tests will be skipped.")

# Import the Flask app 
try:
    from app import app as flask_app
    flask_app.config["TESTING"] = True
    FLASK_AVAILABLE = True
except Exception as _fe:
    print(f"[integration] Flask app import failed: {_fe}")
    FLASK_AVAILABLE = False
