#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 10:28:36 2025
@Task: Initialize section of the Algorithm I
@author: amwangi
"""

import random
import pandas as pd
from ipaddress import ip_network, ip_address
from Observe import current_network_state   #Network Health - OODA framework

def dhcp_network_plan():
    
    '''
        Preliminary I: Subnet Pools, K, for different regions
    '''
    
    subnet_pools = {
        "WTG1": {"subnet": "192.168.16.0/25", "rangeStart": "192.168.16.10", "rangeEnd": "192.168.16.125"},
        "WTG2": {"subnet": "192.168.16.128/25", "rangeStart": "192.168.16.139", "rangeEnd": "192.168.16.253"},
        "WTG3": {"subnet": "192.168.17.0/25", "rangeStart": "192.168.17.10", "rangeEnd": "192.168.17.125"},
        "WTG4": {"subnet": "192.168.17.128/25", "rangeStart": "192.168.17.139", "rangeEnd": "192.168.17.253"},
        "WTG5": {"subnet": "192.168.18.0/25", "rangeStart": "192.168.18.10", "rangeEnd": "192.168.18.125"},
        "WTG6": {"subnet": "192.168.18.128/25", "rangeStart": "192.168.18.139", "rangeEnd": "192.168.18.253"},
        "WTG7": {"subnet": "192.168.19.0/25", "rangeStart": "192.168.19.10", "rangeEnd": "192.168.19.125"},
        "WTG8": {"subnet": "192.168.19.128/25", "rangeStart": "192.168.19.139", "rangeEnd": "192.168.19.253"},
        "WTG9": {"subnet": "192.168.20.0/25", "rangeStart": "192.168.20.10", "rangeEnd": "192.168.20.125"},
        "WTG10": {"subnet": "192.168.20.128/25", "rangeStart": "192.168.20.139", "rangeEnd": "192.168.20.253"},
        "WTG11": {"subnet": "192.168.21.0/25", "rangeStart": "192.168.21.10", "rangeEnd": "192.168.21.125"},
        "WTG12": {"subnet": "192.168.21.128/25", "rangeStart": "192.168.21.139", "rangeEnd": "192.168.21.253"},
        "WTG13": {"subnet": "192.168.22.0/25", "rangeStart": "192.168.22.10", "rangeEnd": "192.168.22.125"},
        "WTG14": {"subnet": "192.168.22.128/25", "rangeStart": "192.168.22.139", "rangeEnd": "192.168.22.253"},
        "WTG15": {"subnet": "192.168.23.0/25", "rangeStart": "192.168.23.10", "rangeEnd": "192.168.23.125"},
        "WTG16": {"subnet": "192.168.23.128/25", "rangeStart": "192.168.23.139", "rangeEnd": "192.168.23.253"},
        "WTG17": {"subnet": "192.168.24.0/25", "rangeStart": "192.168.24.10", "rangeEnd": "192.168.24.125"},
        "WTG18": {"subnet": "192.168.24.128/25", "rangeStart": "192.168.24.139", "rangeEnd": "192.168.24.253"},
        "WTG19": {"subnet": "192.168.25.0/25", "rangeStart": "192.168.25.10", "rangeEnd": "192.168.25.125"},
        "WTG20": {"subnet": "192.168.25.128/25", "rangeStart": "192.168.25.139", "rangeEnd": "192.168.25.253"},
        "Spine_Layer": {"subnet": "192.168.26.0/27", "rangeStart": "192.168.26.10", "rangeEnd": "192.168.26.28"},
        "ECPSC": {"subnet": "192.168.27.0/25", "rangeStart": "192.168.27.10", "rangeEnd": "192.168.27.125"},
        "vPACSC": {"subnet": "192.168.28.0/23", "rangeStart": "192.168.28.10", "rangeEnd": "192.168.29.127"}
    }
    
    
    
    '''
        Preliminary II: Assign each host an IP from the tuple
    '''
    
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
    #To read the host names from this newly developed dataframe use the command `s2h_df_sorted.iloc[:,-1].tolist()`
    
    host_group_mapping = {
        "WTG1": ["r1", "b1", "d1"], 
        "WTG2": ["r2", "b2", "d2"], 
        "WTG3": ["r3", "b3", "d3"],
        "WTG4": ["r4", "b4", "d4"], 
        "WTG5": ["r5", "b5", "d5"], 
        "WTG6": ["r6", "b6", "d6"],
        "WTG7": ["r7", "b7", "d7"], 
        "WTG8": ["r8", "b8", "d8"], 
        "WTG9": ["r9", "b9", "d9"],
        "WTG10": ["r10", "b10", "d10"], 
        "WTG11": ["r11", "b11", "d11"], 
        "WTG12": ["r12", "b12", "d12"],
        "WTG13": ["r13", "b13", "d13"], 
        "WTG14": ["r14", "b14", "d14"], 
        "WTG15": ["r15", "b15", "d15"],
        "WTG16": ["r16", "b16", "d16"], 
        "WTG17": ["r17", "b17", "d17"], 
        "WTG18": ["r18", "b18", "d18"],
        "WTG19": ["r19", "b19", "d19"], 
        "WTG20": ["r20", "b20", "d20"], 
        "Spine_Layer": ["d26", "d25", "d24", "d23"],
        "ECPSC": ["e1", "e2", "e3", "e4", "e5"],
        "vPACSC": ["v1", "v2", "v3", "v4", "v5", "m1", "m2", "m3", "m4", "m5","q1", "q2", "q3", "q4", "q5"]
    }


    return subnet_pools, s2h_df_sorted,host_group_mapping

def get_host_ip_mapping(subnet_pools, host_group_mapping):
    
    """
    Generates a mapping of hosts to their respective subnets and IP addresses.
    
        :param current_network_state: Function to fetch the current network state
        :param subnet_pools: Dictionary containing subnet pools
        :param host_group_mapping: Dictionary mapping hosts to specific groups
        :return: DataFrame containing the mapping of hosts to switches, ports, and assigned IPs  
    """  

    #Preliminary II: Assign each host an IP from the tuple:  HIP = (rIP, vIP1, vIP2)
    assigned_ips = set()  #Stores all assigned IPS globally to avoid overlaps
    host_ip_mapping = {}

    for region, hosts_list in host_group_mapping.items():
        for host in hosts_list:
            # Generate 3 IPs for the host from the subnet pool range
            subnet_info = subnet_pools.get(region)
            ip_range_start = ip_address(subnet_info["rangeStart"])
            ip_range_end = ip_address(subnet_info["rangeEnd"])
            
            available_ips = [str(ip) for ip in ip_network(f'{subnet_info["subnet"]}').hosts() if ip >= ip_range_start and ip <= ip_range_end]
            random.shuffle(available_ips)
            
            # Assign 3 IPs ensuring no overlap
            assigned_ips_for_host = []
            for ip in available_ips:
                if ip not in assigned_ips and len(assigned_ips_for_host) < 3:
                    assigned_ips.add(ip)
                    assigned_ips_for_host.append(ip)
            
            host_ip_mapping[host] = assigned_ips_for_host
            
    return host_ip_mapping

def structuring_host_maps (host_ip_mapping):
    structured_host_ip_mapping = {}   #Create an empty dict to store the properly structured Host IPs
    for host, ip_list in host_ip_mapping.items():
        if len(ip_list) == 3:    #Check if each host already has 3 IP addresses assigned to it already
            structured_host_ip_mapping[host] = {
                "rIP": ip_list[0],  # Real IP
                "vIP1": ip_list[1],  # Virtual IP 1
                "vIP2": ip_list[2]   # Virtual IP 2
                }
            
    return structured_host_ip_mapping

def initialize_mtd():
    subnet_pools , s2h_df_sorted, host_group_mapping = dhcp_network_plan()
    host_ip_mapping = get_host_ip_mapping(subnet_pools, host_group_mapping)
    
    #Merging the two dataframe to one and storing them to a database
    host_ip_df = pd.DataFrame.from_dict(host_ip_mapping,orient='index').reset_index()
    host_ip_df.rename(columns={'index':'host_names'}, inplace=True)
    switch_host_info = s2h_df_sorted.merge(host_ip_df,on='host_names',how='left')
    
    
    #Store this as a time stamped record in the knowledge base
    
    return switch_host_info