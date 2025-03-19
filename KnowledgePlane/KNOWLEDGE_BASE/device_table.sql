CREATE TABLE device_records (
    id VARCHAR(50) PRIMARY KEY,
    type VARCHAR(50),
    available BOOLEAN,
    role VARCHAR(50),
    mfr VARCHAR(255),
    hw VARCHAR(255),
    sw VARCHAR(255),
    serial VARCHAR(255),
    driver VARCHAR(255),
    chassisId VARCHAR(50),
    lastUpdate BIGINT,
    humanReadableLastUpdate VARCHAR(255),
    annotations JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
