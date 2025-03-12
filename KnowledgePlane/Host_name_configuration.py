#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 13:56:27 2025
@Task: Updating Host Names to human readable names
@author: Agrippina Mwangi
"""

import requests
import json

# ONOS Controller credentials
ONOS_IP = "http://10.10.10.43:8181"
USERNAME = "onos"
PASSWORD = "rocks"

# Function to get the list of hosts
def get_hosts():
    url = f"{ONOS_IP}/onos/v1/hosts"
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    
    # Check if the response is successful
    if response.status_code == 200:
        try:
            return response.json()  # Parse the response into JSON (Python dict/list)
        except ValueError:
            print("Error parsing JSON response")
            return []
    else:
        print("Error fetching hosts:", response.status_code)
        return []

# Function to update host with human-readable name
def update_host_name(host_id, human_readable_name):
    url = f"{ONOS_IP}/onos/v1/hosts/{host_id}"
    headers = {"Content-Type": "application/json"}
    
    # Fetch the current host data
    host_data = get_hosts()
    
    # Check if host_data is empty or None
    if not host_data:
        print("No host data found.")
        return

    # Find the host based on host_id
    host = next((h for h in host_data if h['id'] == host_id), None)
    
    if host:
        # Add human-readable name to annotations
        annotations = host.get('annotations', {})
        annotations['name'] = human_readable_name

        # Prepare the updated data
        updated_host_data = {
            "id": host["id"],
            "mac": host["mac"],
            "ipAddresses": host["ipAddresses"],
            "location": host["location"],
            "vlanId": host["vlanId"],
            "annotations": annotations
        }

        # Send the PUT request to update the host
        response = requests.put(url, json=updated_host_data, headers=headers, auth=(USERNAME, PASSWORD))
        
        if response.status_code == 200:
            print(f"Host {host_id} updated successfully!")
        else:
            print(f"Failed to update host {host_id}: {response.status_code}")
    else:
        print("Host not found.")

# Function to ask the user if they want to continue
def ask_to_continue():
    while True:
        user_input = input("Do you wish to configure another host? (yes/no): ").strip().lower()
        if user_input in ["yes", "no"]:
            return user_input == "yes"
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

# Main function to automate host name configuration
def automate_host_name_configuration():
    while True:
        # Ask the user for the host ID and the new human-readable name
        host_id = input("Enter the host ID (e.g., 00:00:00:00:00:38): ").strip()
        human_readable_name = input("Enter the new human-readable name for the host: ").strip()

        # Update the host name
        update_host_name(host_id, human_readable_name)
        
        # Ask if the user wants to continue configuring more hosts
        if not ask_to_continue():
            print("Host configuration process stopped.")
            break

# Run the automation process
automate_host_name_configuration()
