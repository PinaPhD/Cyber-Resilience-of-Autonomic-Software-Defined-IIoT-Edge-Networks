#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Date created on Sun Feb 16 21:26:41 2025
    @Task description: DHCP Server and Relay Agent Configuration
    @author: Agrippina Mwangi
"""

import os
import requests
import json


#DHCP Subnet Pool Configuration
# ONOS REST API Credentials
ONOS_IP = "10.10.10.43"  # Change to your ONOS controller's IP
USERNAME = "onos"
PASSWORD = "rocks"

# API Endpoint for DHCP Configuration
API_URL = f"http://{ONOS_IP}:8181/onos/v1/network/configuration"

# DHCP Configuration with custom subnets and labels for each pool
dhcp_config = {
    "dhcpServers": {
        "dhcpConfig": {
            "defaultGateway": "192.168.16.254",  # Example default gateway; 
            "domainName": "sd-iiot-edge.com",
            # Global subnet mask is less relevant with multiple CIDRs; 
            "subnetMask": "255.255.255.128",
            "dnsServers": ["8.8.8.8"],
            "pools": {
                "192.168.16.0/25": {
                    "label": "WTG1",
                    "rangeStart": "192.168.16.1",
                    "rangeEnd": "192.168.16.126"
                },
                "192.168.16.128/25": {
                    "label": "WTG2",
                    "rangeStart": "192.168.16.129",
                    "rangeEnd": "192.168.16.254"
                },
                "192.168.17.0/25": {
                    "label": "WTG3",
                    "rangeStart": "192.168.17.1",
                    "rangeEnd": "192.168.17.126"
                },
                "192.168.17.128/25": {
                    "label": "WTG4",
                    "rangeStart": "192.168.17.129",
                    "rangeEnd": "192.168.17.254"
                },
                "192.168.18.0/25": {
                    "label": "WTG5",
                    "rangeStart": "192.168.18.1",
                    "rangeEnd": "192.168.18.126"
                },
                "192.168.18.128/25": {
                    "label": "WTG6",
                    "rangeStart": "192.168.18.129",
                    "rangeEnd": "192.168.18.254"
                },
                "192.168.19.0/25": {
                    "label": "WTG7",
                    "rangeStart": "192.168.19.1",
                    "rangeEnd": "192.168.19.126"
                },
                "192.168.19.128/25": {
                    "label": "WTG8",
                    "rangeStart": "192.168.19.129",
                    "rangeEnd": "192.168.19.254"
                },
                "192.168.20.0/25": {
                    "label": "WTG9",
                    "rangeStart": "192.168.20.1",
                    "rangeEnd": "192.168.20.126"
                },
                "192.168.20.128/25": {
                    "label": "WTG10",
                    "rangeStart": "192.168.20.129",
                    "rangeEnd": "192.168.20.254"
                },
                "192.168.21.0/25": {
                    "label": "WTG11",
                    "rangeStart": "192.168.21.1",
                    "rangeEnd": "192.168.21.126"
                },
                "192.168.21.128/25": {
                    "label": "WTG12",
                    "rangeStart": "192.168.21.129",
                    "rangeEnd": "192.168.21.254"
                },
                "192.168.22.0/25": {
                    "label": "WTG13",
                    "rangeStart": "192.168.22.1",
                    "rangeEnd": "192.168.22.126"
                },
                "192.168.22.128/25": {
                    "label": "WTG14",
                    "rangeStart": "192.168.22.129",
                    "rangeEnd": "192.168.22.254"
                },
                "192.168.23.0/25": {
                    "label": "WTG15",
                    "rangeStart": "192.168.23.1",
                    "rangeEnd": "192.168.23.126"
                },
                "192.168.23.128/25": {
                    "label": "WTG16",
                    "rangeStart": "192.168.23.129",
                    "rangeEnd": "192.168.23.254"
                },
                "192.168.24.0/25": {
                    "label": "WTG17",
                    "rangeStart": "192.168.24.1",
                    "rangeEnd": "192.168.24.126"
                },
                "192.168.24.128/25": {
                    "label": "WTG18",
                    "rangeStart": "192.168.24.129",
                    "rangeEnd": "192.168.24.254"
                },
                "192.168.25.0/25": {
                    "label": "WTG19",
                    "rangeStart": "192.168.25.1",
                    "rangeEnd": "192.168.25.126"
                },
                "192.168.25.128/25": {
                    "label": "WTG20",
                    "rangeStart": "192.168.25.129",
                    "rangeEnd": "192.168.25.254"
                },
                "192.168.26.0/27": {
                    "label": "Spine_Layer",
                    "rangeStart": "192.168.26.1",
                    "rangeEnd": "192.168.26.30"
                },
                "192.168.27.0/25": {
                    "label": "ECP_server_cluster",
                    "rangeStart": "192.168.27.1",
                    "rangeEnd": "192.168.27.126"
                },
                "192.168.27.128/25": {
                    "label": "vPAC_server_cluster",
                    "rangeStart": "192.168.27.129",
                    "rangeEnd": "192.168.27.254"
                }
            }
        }
    }
}

# Send the DHCP configuration to ONOS
response = requests.post(
    API_URL,
    auth=(USERNAME, PASSWORD),
    headers={"Content-Type": "application/json"},
    data=json.dumps(dhcp_config)
)

# Print response status
if response.status_code in [200, 204]:
    print("✅ DHCP configuration applied successfully!")
else:
    print(f"❌ Error: {response.status_code}, {response.text}")

# Verifying DHCP Leases
dhcp_leases_url = f"http://{ONOS_IP}:8181/onos/v1/dhcp/allocations"
response = requests.get(dhcp_leases_url, auth=(USERNAME, PASSWORD))

if response.status_code == 200:
    dhcp_leases = response.json()
    print("\n📌 Current DHCP Leases:")
    for lease in dhcp_leases:
        print(f"MAC: {lease.get('mac', 'N/A')} -> IP: {lease.get('ip', 'N/A')}")
else:
    print(f"❌ Error retrieving DHCP leases: {response.status_code}, {response.text}")

