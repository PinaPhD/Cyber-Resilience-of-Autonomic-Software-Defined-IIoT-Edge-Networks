#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 13:35:58 2025

@author: Agrippina Mwangi
"""
<<<<<<< HEAD

#Importing relevant helper functions
import random
import requests
import time


=======
import random
import pandas as pd
>>>>>>> b9230616b02a92a8272fdb682ea3e556df69265b
from Observe import current_network_state   #Loads the current network state as observed real-time




#Preliminary I: Subnet Pools, K, for different regions
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
