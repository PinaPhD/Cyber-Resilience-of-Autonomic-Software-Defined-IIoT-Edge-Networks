CREATE TABLE rhm_mutation_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    host_id VARCHAR(50),
    real_ip VARCHAR(45),
    mutated_vip VARCHAR(45),
    mac_address VARCHAR(50),
    rhm_status VARCHAR(20),
    severity VARCHAR(20),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
