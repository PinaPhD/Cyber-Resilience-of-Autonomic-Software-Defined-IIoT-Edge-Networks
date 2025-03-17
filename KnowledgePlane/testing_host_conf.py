#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 11:09:06 2025

@author: amwangi
"""

import requests

# ONOS Controller Details
ONOS_IP = "10.10.10.43"  # Update if needed
ONOS_PORT = "8181"
ONOS_USER = "onos"
ONOS_PASS = "rocks"

# API Endpoint
BASE_URL = f"http://{ONOS_IP}:{ONOS_PORT}/onos/v1"
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}

# Extracted details for the host (switch_host_info.iloc[0])
switch_id = "of:0000000000000001"
port = 6
mac_address = "00:00:00:00:00:2E"
ip_addresses = ["192.168.26.21", "192.168.26.11", "192.168.26.14"]

# Function to retrieve and remove old flow rules
def remove_old_flows(device_id):
    url = f"{BASE_URL}/flows/{device_id}"
    response = requests.get(url, auth=(ONOS_USER, ONOS_PASS), headers=HEADERS)
    
    if response.status_code == 200:
        flows = response.json().get("flows", [])
        for flow in flows:
            flow_id = flow.get("id")
            del_url = f"{BASE_URL}/flows/{device_id}/{flow_id}"
            del_response = requests.delete(del_url, auth=(ONOS_USER, ONOS_PASS), headers=HEADERS)
            
            if del_response.status_code == 204:
                print(f"Deleted flow {flow_id} from {device_id}")
            else:
                print(f"Error deleting flow {flow_id}: {del_response.status_code}, {del_response.text}")
    else:
        print(f"Error fetching flows: {response.status_code}, {response.text}")

# Function to add new flow rules for updated IPs
def add_host_ip_flow(device_id, mac_address, ip_addresses, port):
    for ip in ip_addresses:
        flow_rule = {
            "priority": 40000,  # Properly placed priority
            "isPermanent": True,
            "deviceId": device_id,
            "treatment": {
                "instructions": [
                    {"type": "OUTPUT", "port": str(port)}
                ]
            },
            "selector": {
                "criteria": [
                    {"type": "ETH_DST", "mac": mac_address},
                    {"type": "IPV4_DST", "ip": f"{ip}/32"}
                ]
            }
        }

        url = f"{BASE_URL}/flows/{device_id}"
        response = requests.post(url, auth=(ONOS_USER, ONOS_PASS), headers=HEADERS, json=flow_rule)

        if response.status_code == 201:
            print(f"Flow added for IP {ip}")
        else:
            print(f"Error adding flow for {ip}: {response.status_code}, {response.text}")

# Execute Flow Update
remove_old_flows(switch_id)  # Remove old flows properly
add_host_ip_flow(switch_id, mac_address, ip_addresses, port)  # Assign new IPs to host

print("Flow update completed.")

