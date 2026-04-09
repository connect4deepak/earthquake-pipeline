
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
