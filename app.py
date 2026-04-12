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

# Routes 
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stats")
def api_stats():
    stats = query_one(f"""
        SELECT
            COUNT(*)                                        AS total_processed,
            ROUND(AVG(magnitude)::numeric, 2)               AS avg_magnitude,
            ROUND(MAX(magnitude)::numeric, 2)               AS max_magnitude,
            ROUND(MIN(magnitude)::numeric, 2)               AS min_magnitude,
            ROUND(AVG(depth_km)::numeric, 2)                AS avg_depth_km,
            ROUND(MAX(depth_km)::numeric, 2)                AS max_depth_km,
            ROUND(AVG(distance_from_ref_km)::numeric, 0)    AS avg_distance_km,
            0 AS outlier_count,
            MIN(event_time)                                 AS earliest_event,
            MAX(event_time)                                 AS latest_event
        FROM {PROCESSED_TABLE};
    """)

    raw = query_one(f"SELECT COUNT(*) AS raw_count FROM {RAW_TABLE};")
    stats["raw_count"] = raw.get("raw_count", 0)
    # Serialise datetimes
    for k, v in stats.items():
        if isinstance(v, datetime):
            stats[k] = v.isoformat()
    return jsonify(stats)

@app.route("/api/charts")
def api_charts():

    # Magnitude category counts
    mag_cats = query_db(f"""
        SELECT mag_category, COUNT(*) AS count
        FROM {PROCESSED_TABLE}
        GROUP BY mag_category
        ORDER BY CASE mag_category
            WHEN 'micro'    THEN 1 WHEN 'minor'    THEN 2 WHEN 'light'   THEN 3
            WHEN 'moderate' THEN 4 WHEN 'strong'   THEN 5 WHEN 'major'   THEN 6
            WHEN 'great'    THEN 7 ELSE 8 END;
    """)
    # Depth category counts
    depth_cats = query_db(f"""
        SELECT depth_category, COUNT(*) AS count
        FROM {PROCESSED_TABLE}
        GROUP BY depth_category
        ORDER BY CASE depth_category
            WHEN 'shallow' THEN 1 WHEN 'intermediate' THEN 2 WHEN 'deep' THEN 3 END;
    """)