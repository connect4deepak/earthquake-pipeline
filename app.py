import sys
import os
import json
import subprocess
from datetime import datetime, timezone
from flask import Flask, render_template, jsonify, request
import psycopg2
import psycopg2.extras

PIPELINE_DIR = "/home/ubuntu/earthquake-pipelibe"
sys.path.insert(0, PIPELINE_DIR)
from config import DB_CONFIG, PROCESSED_TABLE, RAW_TABLE
app = Flask(__name__)

# DB helper functions  
def query_db(sql: str, params=None) -> list[dict]:
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params or ())
            return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()

def query_one(sql: str, params=None) -> dict:
    rows = query_db(sql, params)
    return rows[0] if rows else {}