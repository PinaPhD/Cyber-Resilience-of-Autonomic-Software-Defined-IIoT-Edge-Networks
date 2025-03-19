CREATE TABLE IF NOT EXISTS port_statistics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    port INT NOT NULL,
    device VARCHAR(255) NOT NULL,
    packetsReceived BIGINT,
    packetsSent BIGINT,
    bytesReceived BIGINT,
    bytesSent BIGINT,
    packetsRxDropped BIGINT,
    packetsTxDropped BIGINT,
    packetsRxErrors BIGINT,
    packetsTxErrors BIGINT,
    durationSec BIGINT,
    bytesReceivedRate DOUBLE, -- bytes received per second
    bytesSentRate DOUBLE, -- bytes sent per second
    packetsReceivedRate DOUBLE, -- packets received per second
    packetsSentRate DOUBLE -- packets sent per second

);