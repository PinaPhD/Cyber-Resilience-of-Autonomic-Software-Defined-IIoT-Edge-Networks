CREATE TABLE IF NOT EXISTS link_records (
    src_device VARCHAR(255) NOT NULL,
    src_port VARCHAR(10) NOT NULL,
    dst_device VARCHAR(255) NOT NULL,
    dst_port VARCHAR(10) NOT NULL,
    type VARCHAR(50),
    state VARCHAR(50),
    PRIMARY KEY (src_device, src_port, dst_device, dst_port)  -- Prevents duplicates
);
