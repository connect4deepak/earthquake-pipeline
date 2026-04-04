import logging
import numpy as np
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from sqlalchemy import create_engine
from config import DB_CONFIG, RAW_TABLE, PROCESSED_TABLE

logger = logging.getLogger(__name__)

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_engine():
    c = DB_CONFIG
    url = (f"postgresql+psycopg2://{c['user']}:{c['password']}"
           f"@{c['host']}:{c['port']}/{c['dbname']}")
    return create_engine(url)

# Read
def load_raw_earthquakes() -> pd.DataFrame:
    query = f"SELECT * FROM {RAW_TABLE};"
    df = pd.read_sql(query, get_engine())
    logger.info(f"Loaded {len(df):,} rows from '{RAW_TABLE}'.")
    return df

def load_new_earthquakes(since_id: int = 0) -> pd.DataFrame:
    query = f"SELECT * FROM {RAW_TABLE} WHERE id > %(sid)s ORDER BY id;"
    df = pd.read_sql(query, get_engine(), params={"sid": since_id})
    logger.info(f"Loaded {len(df):,} new rows (id > {since_id}).")
    return df

def get_last_processed_id() -> int:
    query = f"SELECT COALESCE(MAX(raw_id), 0) FROM {PROCESSED_TABLE};"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchone()[0]
 