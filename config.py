DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "earthquake_db",
    "user":     "root",
    "password": "root",   # ← update this
}

# Raw table written by cron job
RAW_TABLE = "earthquakes"
# Output table for the processed and feature-engineered data
PROCESSED_TABLE = "earthquakes_processed"

#  Cleaning thresholds
MAGNITUDE_MIN   = -2.0  
MAGNITUDE_MAX   = 10.0  
DEPTH_MIN_KM    = 0.0
DEPTH_MAX_KM    = 700.0 
LAT_RANGE       = (-90.0,  90.0)
LON_RANGE       = (-180.0, 180.0)

# IQR multiplier for outlier detection (1.5 = standard, 3.0 = conservative)
IQR_MULTIPLIER  = 1.5

# Reference point for distance feature 
REFERENCE_LAT   = 53.3498
REFERENCE_LON   = -6.2603
REFERENCE_LABEL = "Dublin, Ireland"