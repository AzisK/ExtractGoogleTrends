CREATE TABLE IF NOT EXISTS google_trends (
    datestamp DATE,
    query VARCHAR,
    cnt INT,
    created_timestamp TIMESTAMP,
    modified_timestamp TIMESTAMP
);
