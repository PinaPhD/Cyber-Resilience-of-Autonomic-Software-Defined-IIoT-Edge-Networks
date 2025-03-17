#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 08:19:23 2025

@author: amwangi
"""
import random
from ipaddress import ip_network, ip_address

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