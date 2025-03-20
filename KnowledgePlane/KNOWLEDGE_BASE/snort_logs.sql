CREATE TABLE snort_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    IDS_node VARCHAR(50),         -- The IDS node (d1, d2, ..., d26)
    src_ip VARCHAR(45),           -- Attacker's IP
    src_port INT,                 -- Source port
    dest_ip VARCHAR(45),          -- Target IP
    dest_port INT,                -- Target port
    protocol VARCHAR(10),         -- TCP, UDP, ICMP, etc.
    msg TEXT,                     -- Snort rule alert message
    sid INT,                      -- Snort rule ID
    rev INT,                      -- Rule version
    classtype VARCHAR(50),        -- Classification type
    cve_id VARCHAR(30),           -- CVE reference
    mitre_attack VARCHAR(30),     -- MITRE ATT&CK reference
    raw_log TEXT                   -- Original log entry
);
