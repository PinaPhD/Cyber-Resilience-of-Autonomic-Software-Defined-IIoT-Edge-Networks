#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to update host details using ONOS NetCfg API.
"""

import requests
import json

# ONOS API Details
ONOS_URL = "http://10.10.10.43:8181/onos/v1/network/configuration/"
AUTH = ("onos", "rocks")

# Define the host ID to update (must match format exactly)
host_id = "00:00:00:00:00:34/None"  # Example host ID

# Network Configuration Data (matching ONOS official format)
netcfg_data = {
    host_id: {  # Host MAC address with "/None" suffix
        "basic": {
            "ips": ["192.168.29.30", "192.168.28.162", "192.168.28.90"],  # Assign new IPs
            "locations": ["of:0000000000000009/2"]  # Example switch ID and port
        }
    }
}

# Convert data to JSON format
json_data = json.dumps(netcfg_data)

# Send POST request to update host configuration
response = requests.post(ONOS_URL, data=json_data, headers={"Content-Type": "application/json"}, auth=AUTH)

# Check response
if response.status_code in [200, 204]:
    print("Host configuration updated successfully via NetCfg API.")
else:
    print(f"Failed to update host. Status Code: {response.status_code}, Response: {response.text}")
