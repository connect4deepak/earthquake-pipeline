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
        
# Write
def _to_native(val):

    if isinstance(val, np.integer):
        return int(val)
    if isinstance(val, np.floating):
        return None if np.isnan(val) else float(val)
    if isinstance(val, np.bool_):
        return bool(val)
    if isinstance(val, float) and np.isnan(val):
        return None
    return val

def save_processed(df: pd.DataFrame) -> None:

    if df.empty:
        logger.warning("save_processed called with empty DataFrame — skipping.")
        return
    df = df.copy()
    for col in df.columns:
        df[col] = df[col].apply(_to_native)

    cols = list(df.columns)
    rows = [tuple(r) for r in df.itertuples(index=False)]
    update_cols = [c for c in cols if c != "raw_id"]
    update_clause = ", ".join(f"{c} = EXCLUDED.{c}" for c in update_cols)

    insert_sql = f"""
        INSERT INTO {PROCESSED_TABLE} ({', '.join(cols)})
        VALUES %s
        ON CONFLICT (raw_id) DO UPDATE SET {update_clause};
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            execute_values(cur, insert_sql, rows)
        conn.commit()

    logger.info(f"Upserted {len(df):,} rows into '{PROCESSED_TABLE}'.")
