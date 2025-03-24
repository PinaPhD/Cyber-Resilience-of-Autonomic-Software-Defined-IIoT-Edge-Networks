#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Fri Feb 21 13:35:58 2025
    @Task: Event triggered moving target defense module running at the Knowledge Plane of the Software-defined IIoT-Edge network
    @author: Agrippina Mwangi
"""

import random
import requests
import time
import json
import numpy as np
import pandas as pd
from requests.auth import HTTPBasicAuth
from ipaddress import ip_network, ip_address
from Initialize import initialize_mtd
from Initialize import dhcp_network_plan
from Observe import current_network_state   #Network Health - OODA framework
from Orient import get_cvss_scores
from datetime import datetime, timedelta
import mysql.connector

'''
    Initialize section ---> In the Initialize_mtd() function
        :Param - subnet pools, K, for different regions
        :Param - Assign each host an IP from the tuple
        :Param - configure micro-segmentation "Intents" --- Linking to the ACT Module
        :Param - Compute the Risk Score (Rh)
'''

#Connecting to the knowledge base
DB_HOST = "10.10.10.30"
DB_USER = "pina254"
DB_PASSWORD = "Baarn@2026_"
DB_NAME = "KNOWLEDGE_BASE"

switch_host_info = initialize_mtd()  #Defining host dictionary structured as a tuple comprising (rIP, vIP1, vIP2)
host_group_mapping = dhcp_network_plan()  #To access subnet pools and host group mapping
devices, links, hosts, flows, port_stats, snort_logs = current_network_state() #Reading the current network state

#Store all the assigned IPs to avoid reusing them
assigned_ips = set(switch_host_info[0].tolist() + switch_host_info[1].tolist() + switch_host_info[2].tolist())

'''
STEP 3/4: Read CVSS from threat intelligence sources and determining the threat severity (Z)
--- ORIENT MODULE
'''

threat_map = get_cvss_scores()
for cve, details in threat_map.items():
    print(f"{cve}: CVSS={details['cvss_score']} | Severity={details['severity_label']} ({details['severity_value']})")

def log_mutation_event_to_mysql(host_id, rIP, new_vIP, vMAC, rho_rhm, severity_level):
    #connect to the MYSQL server running on port 
    conn = None
    cursor = None

    try:
        # Establish database connection
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        query = """
        INSERT INTO rhm_mutation_log
        (host_id, real_ip, mutated_vip, mac_address, rhm_status, severity, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        values = (host_id, rIP, new_vIP, vMAC, rho_rhm, severity_level, timestamp)

        cursor.execute(query, values)
        conn.commit()

        print(f">> [LOG] Mutation event stored in MySQL for {host_id}")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f">> [ERROR] Failed to log to MySQL: {err}")
        
    
def perform_ofrhm(host_info):
    print(">> [ACTION] Performing OF-RHM on", host_info)
    for index, row in host_info.iterrows():
        host_name = row['host_names']
        rIP = row[0]
        vIP1 = row[1]
        vIP2 = row[2]
        
        #Now, lets determine the target region based on the IP_dst information based on the multi-log ingestion analysis
        region = None
        for reg, hosts in host_group_mapping.items():
            if host_name in hosts:
                region = reg
                break
            
        #It is my sincere hope that we never get this message  :-) LOL 
        if not region:
            print(f">> [OF-RHM] Region not found for host {host_name}. Skipping.")
            continue
        
        subnet_info = dhcp_network_plan()[0][region]
        ip_range_start = ip_address(subnet_info["rangeStart"])
        ip_range_end = ip_address(subnet_info["rangeEnd"])
        subnet_ips = [str(ip) for ip in ip_network(subnet_info["subnet"]).hosts()
                      if ip_range_start <= ip <= ip_range_end]
        
        #Storing the available IP pool
        available_ips = [ip for ip in subnet_ips if ip not in assigned_ips]
        
        if not available_ips:
            print(f">> [OF-RHM] No available IPs in pool for host {host_name}. Mutation skipped.")
            continue
        
        new_ip =random.choice(available_ips)
        assigned_ips.add(new_ip)  # Mark as used
        print(f">> [OF-RHM] Host {host_name} (rIP: {rIP}) mutated to {new_ip} in region {region}")
        
        return new_ip    #This should go to the mutation record and to the ACT Module for update in the Control Plane Flow Rule and Intents Data Store

def isolate_host(host_info):
    print(">> [ACTION] Isolating host", host_info)

def block_source_ip(host_info):
    print(">> [ACTION] Blocking source IP", host_info)

def notify_admin(cve_id, severity_label):
    print(f">> [NOTIFY] Admin notified of {severity_label.upper()} threat: {cve_id}")

def log_incident(cve_id, severity_label):
    print(f">> [LOG] Incident logged: {cve_id} ({severity_label})")

def increase_flow_timeout():
    print(">> [ACTION] Flow timeout increased.")

def increase_monitoring_flow():
    print(">> [ACTION] Monitoring frequency increased on affected flows.")

def log_forensics(cve_id):
    print(f">> [LOG] {cve_id} flagged for manual review/forensics.")

def is_network_degraded():
    # Placeholder: in practice, check CPU/mem/traffic stats
    return random.choice([True, False])


'''
STEP 5: 
    Designing the adaptive actions (OpenFlow-based random host mutation for targetted regions) based on the threat severity level
    :Param - Critical == Perform immediate OF-RHM + isolate hosts and block the source IP (where the attacker is)
    :Param - High == Activate OF-RHM + increase flow timeout + notify admin
    :Param - Medium == Log incident + increase monitoring frequency on the flow + Network Health based OF-RHM
    :Param - Low == Log incident + Network-health based OF-RHM + Notify admin
    :Param - None == Continue monitoring 
    :Param - Unkwown == Log incident for forensics or manual review by admin
'''


def response_to_threat(cve_id, severity_label, host_info):
    print(f"\n[DEFENSE] Responding to {cve_id} with severity '{severity_label}'")
    
    if severity_label == "critical":
        print("CRITICAL STATE: Immediately trigger OF-RHM, isolate target host(IP_dst), and block attacker host (IP_src)")
        perform_ofrhm(host_info)   
        isolate_host(host_info)
        block_source_ip(host_info)
        
    elif severity_label == "high":
        print("HIGH: Trigger OF-RHM + increase flow timeout + notify admin")
        perform_ofrhm(host_info)
        increase_flow_timeout()
        notify_admin(cve_id, severity_label)
    
    elif severity_label == "medium":
        log_incident(cve_id, severity_label)
        increase_monitoring_flow()
        if is_network_degraded():
            perform_ofrhm(host_info)
        notify_admin(cve_id, severity_label)
        
    elif severity_label == "none":
        print("None: Continue Monitoring.")
        
    elif severity_label == "Unknown":
        print("Unknown: Log for forensics.")
        log_forensics(cve_id)
        
    else:
        print("Unknown severity level encountered")
        
