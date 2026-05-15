CREATE TABLE etl_control (
    pipeline_id SERIAL PRIMARY KEY,
    pipeline_name VARCHAR,
    source_type VARCHAR,
    source_options JSONB,
    destination_table VARCHAR,
    load_type VARCHAR,
    incremental_key VARCHAR,
    dependencies TEXT[],
    is_active BOOLEAN
);

CREATE TABLE etl_audit_log (
    run_id SERIAL PRIMARY KEY,
    pipeline_name VARCHAR,
    start_time TIMESTAMPTZ,
    end_time TIMESTAMPTZ,
    duration_ms INTEGER,
    status VARCHAR,
    rows_read INTEGER,
    rows_written INTEGER,
    error_message TEXT
);

CREATE TABLE etl_watermarks (
    pipeline_name VARCHAR PRIMARY KEY,
    watermark_value VARCHAR
);

-- Sample source table
CREATE TABLE source_products (
    id INT,
    name TEXT,
    last_modified TIMESTAMP
);

INSERT INTO source_products VALUES
(1,'A','2024-01-01'),
(2,'B','2024-01-02');

-- Pipelines
INSERT INTO etl_control VALUES
(1,'pipeline-A','db','{"table":"source_products"}','dest_a','full',NULL,NULL,TRUE),
(2,'pipeline-B','csv','{"path":"/data/source_data.csv"}','dest_b','full',NULL,ARRAY['pipeline-A'],TRUE),
(3,'pipeline-C','api','{"url":"http://mock-api:8080/data"}','dest_c','incremental','last_modified',NULL,TRUE),
(4,'cycle-A','db','{"table":"source_products"}','dest_d','full',NULL,ARRAY['cycle-B'],TRUE),
(5,'cycle-B','db','{"table":"source_products"}','dest_e','full',NULL,ARRAY['cycle-A'],TRUE);