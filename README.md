# Earthquake Data Acquisition & Preprocessing Pipeline
Python pipeline that reads raw earthquake data collected from the
USGS FDSNWS API, cleans it, analytical features, applies
transformations, and writes the result to a PostgreSQL table ready for
analytics and visualisation.

## Live Dashboard — http://54.247.209.107:8080/

# Earthquake Classification Guide

## Magnitude Category
**Richter / Moment-Magnitude Labels (USGS):**

| Magnitude Range | Category  | Description |
|-----------------|----------|-------------|
| < 2.0           | Micro    | Not felt by people |
| 2.0 – 3.9       | Minor    | Felt slightly by some |
| 4.0 – 4.9       | Light    | Felt by most, minor damage |
| 5.0 – 5.9       | Moderate | Slight damage to buildings |
| 6.0 – 6.9       | Strong   | Destructive in populated areas |
| 7.0 – 7.9       | Major    | Serious damage over large areas |
| ≥ 8.0           | Great    | Total destruction, tsunamis possible |

## Depth Category
**Standard USGS Seismological Classification:**

| Depth Range | Category      | Description |
|------------|--------------|-------------|
| 0 – 70 km  | Shallow      | Causes most damage (closest to surface) |
| 70 – 300 km| Intermediate | Reduced but still significant surface impact |
| > 300 km   | Deep         | Rarely causes surface damage |

app.py — Earthquake Pipeline Flask Dashboard
============================================
Routes
  GET  /              → main dashboard (stats + charts)
  GET  /api/stats     → KPI summary (counts, avg/max magnitude, depth, distance)
  GET  /api/charts    → Chart data (mag/depth categories, hourly, timeline, histogram)
  GET  /api/table     → Paginated processed data with mag/depth filters
  GET  /api/map.      → Latest 1000 events for map (lat, lon, magnitude, place) 
  POST /api/run.      → Trigger pipeline run (`{"mode": "incremental" \| "full"}`) 
  POST /api/run-tests → Run test suite (`{"test_file": "all" \| "transforms" \| "integration"}`) 
"""

## Architecture
```
earthquakes  (raw table, filled by cron job)

# cleaning.py
Stage 1 — Cleaning & Validation            
• Schema normalisation                     
• Type coercion                            
• Null handling & required-field checks    
• Physical range validation                
• Duplicate removal                        
• IQR outlier flagging                     

# features.py
Stage 2 — Feature Engineering            
• Calendar decomposition (year/month)         
• Magnitude category (micro → great)       
• Depth category (shallow/inter/deep)      
• Great-circle distance from reference pt  

#transforms.py
Stage 3 — Transformations                  
• Min-Max scaling (magnitude, depth)    
• One-hot encoding (mag_type)              
• Ordered categorical (mag_/depth_cat)             

earthquakes_processed  (analytics-ready table)
```

## File Structure
```
earthquake_pipeline/
 config.py           # DB credentials & thresholds
 db.py               # PostgreSQL read / write helpers
 cleaning.py         # Stage 1 — Cleaning & Validation
 features.py         # Stage 2 — Feature Engineering
 transforms.py       # Stage 3 — Scaling & Encoding
 pipeline.py         # Main orchestrator (entry point)
 schema.sql          # earthquakes_processed table
 requirements.txt    # Python dependencies
 test_transforms.py  # Unit tests — transforms stage 
 test_integration.py # Integration tests — Flask API endpoints 
 README.md           
```

## Setup

```bash
# 1. Activate your virtual environment
source /home/deepak/venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Edit config.py — update DB_CONFIG password and REFERENCE_LAT/LON

# 4. Create the processed table (one-time)
python pipeline.py --setup
# or directly in psql:
# psql -U postgres -d earthquake -f schema.sql

# Run all tests
python -m unittest test_transforms test_integration -v

# Run only transform unit tests
python test_transforms.py -v

# Run only integration tests (requires live DB + Flask app)
python test_integration.py -v
```

From the dashboard UI, use the **Test Runner** section at the bottom of the page — select a suite and click **RUN TESTS** to see per-test results and raw output inline.

## Running the Pipeline

```bash
# Full run — process every row in the raw table
python pipeline.py

# Incremental run — only rows added since the last pipeline run
python pipeline.py --incremental
```

### Add to crontab (run 5 minutes after the data-fetch cron job)
```cronjob
# Data fetch  — every minute 
*/1 * * * * /home/deepak/venv/bin/python /home/deepak/earthquake-pipeline/fetch_earthquakes.py

# Pipeline    — every minute
*/1 * * * * /home/deepak/venv/bin/python /home/deepak/earthquake_pipeline/pipeline.py --incremental >> /var/log/eq_pipeline.log 2>&1
```

## Features Produced
| Column | Type | Description |
|---|---|---|
| `year` / `month` / `hour` | int | Calendar decomposition |
| `day_of_week` | int | 0 = Monday, 6 = Sunday |
| `is_weekend` | bool | Saturday or Sunday |
| `hour_sin` / `hour_cos` | float | Cyclic hour encoding |
| `month_sin` / `month_cos` | float | Cyclic month encoding |
| `mag_category` | text | micro / minor / light / moderate / strong / major / great |
| `depth_category` | text | shallow / intermediate / deep |
| `distance_from_ref_km` | float | Great-circle km from reference point |
| `magnitude_scaled` | float | Min-Max normalised magnitude [0,1] |
| `depth_scaled` | float | Min-Max normalised depth [0,1] |
| `latitude_scaled` | float | Min-Max normalised latitude [0,1] |
| `longitude_scaled` | float | Min-Max normalised longitude [0,1] |
| `magtype_ml` … | int | One-hot encoded magnitude type |
| `is_outlier` | bool | IQR outlier flag (row kept, not dropped) |