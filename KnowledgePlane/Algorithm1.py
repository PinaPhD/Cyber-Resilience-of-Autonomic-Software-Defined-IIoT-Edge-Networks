#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 13:35:58 2025

@author: Agrippina Mwangi
"""

#Importing relevant helper functions
import random
import requests
import time
import numpy as np
import pandas as pd
from Observe import current_network_state   #Loads the current network state as observed real-time


'''
Preliminary I: Subnet Pools, K, for different regions
'''

subnet_pools = {
    "WTG1": {"subnet": "192.168.16.0/25", "rangeStart": "192.168.16.10", "rangeEnd": "192.168.16.126"},
    "WTG2": {"subnet": "192.168.16.128/25", "rangeStart": "192.168.16.139", "rangeEnd": "192.168.16.254"},
    "WTG3": {"subnet": "192.168.17.0/25", "rangeStart": "192.168.17.10", "rangeEnd": "192.168.17.126"},
    "WTG4": {"subnet": "192.168.17.128/25", "rangeStart": "192.168.17.139", "rangeEnd": "192.168.17.254"},
    "WTG5": {"subnet": "192.168.18.0/25", "rangeStart": "192.168.18.10", "rangeEnd": "192.168.18.126"},
    "WTG6": {"subnet": "192.168.18.128/25", "rangeStart": "192.168.18.139", "rangeEnd": "192.168.18.254"},
    "WTG7": {"subnet": "192.168.19.0/25", "rangeStart": "192.168.19.10", "rangeEnd": "192.168.19.126"},
    "WTG8": {"subnet": "192.168.19.128/25", "rangeStart": "192.168.19.139", "rangeEnd": "192.168.19.254"},
    "WTG9": {"subnet": "192.168.20.0/25", "rangeStart": "192.168.20.10", "rangeEnd": "192.168.20.126"},
    "WTG10": {"subnet": "192.168.20.128/25", "rangeStart": "192.168.20.139", "rangeEnd": "192.168.20.254"},
    "WTG11": {"subnet": "192.168.21.0/25", "rangeStart": "192.168.21.10", "rangeEnd": "192.168.21.126"},
    "WTG12": {"subnet": "192.168.21.128/25", "rangeStart": "192.168.21.139", "rangeEnd": "192.168.21.254"},
    "WTG13": {"subnet": "192.168.22.0/25", "rangeStart": "192.168.22.10", "rangeEnd": "192.168.22.126"},
    "WTG14": {"subnet": "192.168.22.128/25", "rangeStart": "192.168.22.139", "rangeEnd": "192.168.22.254"},
    "WTG15": {"subnet": "192.168.23.0/25", "rangeStart": "192.168.23.10", "rangeEnd": "192.168.23.126"},
    "WTG16": {"subnet": "192.168.23.128/25", "rangeStart": "192.168.23.139", "rangeEnd": "192.168.23.254"},
    "WTG17": {"subnet": "192.168.24.0/25", "rangeStart": "192.168.24.10", "rangeEnd": "192.168.24.126"},
    "WTG18": {"subnet": "192.168.24.128/25", "rangeStart": "192.168.24.139", "rangeEnd": "192.168.24.254"},
    "WTG19": {"subnet": "192.168.25.0/25", "rangeStart": "192.168.25.10", "rangeEnd": "192.168.25.126"},
    "WTG20": {"subnet": "192.168.25.128/25", "rangeStart": "192.168.25.139", "rangeEnd": "192.168.25.254"},
    "Spine_Layer": {"subnet": "192.168.26.0/27", "rangeStart": "192.168.26.10", "rangeEnd": "192.168.26.30"},
    "ECPSC": {"subnet": "192.168.27.0/25", "rangeStart": "192.168.27.10", "rangeEnd": "192.168.27.126"},
    "vPACSC": {"subnet": "192.168.27.128/25", "rangeStart": "192.168.27.139", "rangeEnd": "192.168.27.254"}
}

#Mapping the hosts to the respective regions based on the switch ports
devices, links, hosts, flows, port_stats = current_network_state() 

switch_to_host_mapping = []   #Store the switch to host mapping

for index,row in hosts.iterrows():
    if row["locations"]:
        switch_id= row["locations"][0]["elementId"]
        port = row["locations"][0]["port"]
        host_id = row["id"]
        switch_to_host_mapping.append({"switch_id": switch_id, "port": port, "host_id": host_id})

s2h_df = pd.DataFrame(switch_to_host_mapping)

#Sorting the dataframe by switch id 
s2h_df_sorted = s2h_df.sort_values(by="switch_id").reset_index(drop=True)

#Checking the host annotations from the Mininet network links mapping
host_names = ['d26', 'd25', 'd24', 'd23', 'm1', 'm2', 'd21', 'e3', 'm3', 'v2', 'v1', 'm4', 'm5',
 'e5', 'q1', 'v3', 'q2', 'd22', 'q3', 'q4', 'v4', 'q5', 'e4', 'v5', 'e1', 'e2', 'b1',
 'r1', 'd1', 'r2', 'd2', 'b2', 'b3', 'r3', 'd3', 'r4', 'b4', 'd4', 'b5', 'd5', 'r5',
 'r6', 'b6', 'd6', 'r7', 'd7', 'b7', 'b8', 'r8', 'd8', 'd9', 'r9', 'b9', 'd10', 'r10',
 'b10', 'd11', 'r11', 'b11', 'r12', 'd12', 'b12', 'd13', 'b13', 'r13', 'r14', 'd14',
 'b14', 'b15', 'd15', 'r15', 'd16', 'b16', 'r16', 'r17', 'd17', 'b17', 'r18', 'd18',
 'b18', 'r19', 'b19', 'd19', 'b20', 'r20', 'd20']


#Appending them to the switch/port to host mapping on column host_names
s2h_df_sorted['host_names']=host_names


'''
Preliminary II: Assign each host an IP from the tuple:
HIP = (rIP, vIP1, vIP2)
'''

