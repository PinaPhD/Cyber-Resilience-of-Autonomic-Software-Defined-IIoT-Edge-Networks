#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 20:27:17 2025
Event triggered moving target defense module running at the Knowledge Plane of the Software-defined IIoT-Edge network
@author: agrippina Mwangi
"""

import requests
import time
import logging
import pandas as pd
from datetime import datetime
import json  # Import JSON module to convert dict to string



'''
        ONOS SDN controller cluster interacting with the Knowledge Base
        Connecting to the primary SDN controller using a 8181 RESTful API based url and 
        BASE24 Authentication (Plain user/password credentials)
'''


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Prompting user for ONOS controller details
print("OBSERVE MODULE AS(n) OT Network Topology.\n Disclaimer: Press Enter if you wish to use the default configurations\n\n")
controller_ip = input("Enter the IP address of the ONOS controller (default is 10.10.10.43: )")
controller_ip = controller_ip if controller_ip else '10.10.10.43'
onos_base_url = f'http://{controller_ip}:8181/onos/v1'

username = input("Enter the username for ONOS controller (default is 'onos'): ")
username = username if username else 'onos'
password = input("Enter the password for ONOS controller (default is 'rocks'): ")
password = password if password else 'rocks'
onos_auth = (username, password)


def get_devices():
    """ 
        Fetches network devices from the ONOS controller. 
    """
    
    try:
        response = requests.get(f'{onos_base_url}/devices', auth=onos_auth)
        if response.status_code == 200:
            devices = response.json().get('devices', [])
            df = pd.DataFrame(devices)
            return df
        else:
            print(f"Failed to retrieve Network devices: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching Network devices: {e}")

def get_links():
    """ 
        Fetches network links from the ONOS controller. 
    """
    
    try:
        response = requests.get(f'{onos_base_url}/links', auth=onos_auth)
        if response.status_code == 200:
            links = response.json().get('links', [])
            df = pd.DataFrame(links)
            return df
        else:
            print(f"Failed to retrieve Network links: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching Network Links: {e}")

def get_hosts():
    """ 
        Fetches network hosts from the ONOS controller. 
    """

    try:
        response = requests.get(f'{onos_base_url}/hosts', auth=onos_auth)
        if response.status_code == 200:
            hosts = response.json().get('hosts', [])
            df = pd.DataFrame(hosts)
            return df
        else:
            print(f"Failed to retrieve Network hosts: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching Network hosts: {e}")

def get_flows():
    """ 
        Fetches flow rules from the ONOS controller. 
    """
    
    try:
        response = requests.get(f'{onos_base_url}/flows', auth=onos_auth)
        if response.status_code == 200:
            flows = response.json().get('flows', [])
            df = pd.DataFrame(flows)
            return df
        else:
            print(f"Failed to retrieve Network flows: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching Network flows: {e}")

def get_port_statistics():
    """ 
        Fetches port statistics from all devices in the ONOS controller. 
    """
    
    try:
        response = requests.get(f'{onos_base_url}/statistics/ports', auth=onos_auth)
        if response.status_code == 200:
            port_stats = response.json().get('statistics', [])
            # Flatten the nested JSON structure for easier CSV writing
            flattened_stats = []
            for device in port_stats:
                device_id = device['device']
                for port in device['ports']:
                    port['device'] = device_id
                    flattened_stats.append(port)
            df = pd.DataFrame(flattened_stats)
            return df
        else:
            print(f"Failed to retrieve Port Statistics: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching network port statistics: {e}")


def current_network_state():
    devices = get_devices()
    links = get_links()
    hosts = get_hosts()
    flows = get_flows()
    port_stats = get_port_statistics()
       
    return devices, links, hosts, flows, port_stats



if __name__ == "__main__":
    # Reading the current network state
    devices, links, hosts, flows, port_stats = current_network_state()
    