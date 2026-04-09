
CREATE TABLE IF NOT EXISTS earthquakes_processed (

    -- Identity 
    raw_id                  BIGINT          PRIMARY KEY,   
    -- Cleaned core fields 
    magnitude               NUMERIC(5,2)    NOT NULL,
    latitude                NUMERIC(9,5)    NOT NULL,
    longitude               NUMERIC(9,5)    NOT NULL,
    depth_km                NUMERIC(8,3)    NOT NULL,
    event_time              TIMESTAMPTZ     NOT NULL,
    place                   TEXT,
    mag_type                TEXT,
    event_type              TEXT,
    status                  TEXT,

    -- Time features 
    year                    SMALLINT,
    month                   SMALLINT,       
    day_of_week             SMALLINT,       
    hour                    SMALLINT,       
    is_weekend              BOOLEAN,
    hour_sin                NUMERIC(10,8),
    hour_cos                NUMERIC(10,8),
    month_sin               NUMERIC(10,8),
    month_cos               NUMERIC(10,8),

    -- Engineered features 
    mag_category            TEXT,
        -- CHECK (mag_category IN ('micro','minor','light','moderate','strong','major','great')),
    depth_category          TEXT,
        -- CHECK (depth_category IN ('shallow','intermediate','deep')),
    distance_from_ref_km    NUMERIC(10,3),
    is_outlier              BOOLEAN         DEFAULT FALSE,

    -- Scaled numerics 
    magnitude_scaled        NUMERIC(10,6),
    depth_scaled            NUMERIC(10,6),
    latitude_scaled         NUMERIC(10,6),
    longitude_scaled        NUMERIC(10,6),
