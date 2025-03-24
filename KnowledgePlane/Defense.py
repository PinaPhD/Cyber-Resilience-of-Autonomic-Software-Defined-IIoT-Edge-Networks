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
from Observe import current_network_state   #Network Health - OODA framework
from Orient import get_cvss_scores

'''
    Initialize section ---> In the Initialize_mtd() function
        :Param - subnet pools, K, for different regions
        :Param - Assign each host an IP from the tuple
        :Param - configure micro-segmentation "Intents" --- Linking to the ACT Module
        :Param - Compute the Risk Score (Rh)
'''

#Defining host dictionary structured as a tuple comprising (rIP, vIP1, vIP2)
switch_host_info = initialize_mtd()

#Reading the current network state
devices, links, hosts, flows, port_stats, snort_logs = current_network_state() 

'''
STEP 3/4: Read CVSS from threat intelligence sources and determining the threat severity (Z)
--- ORIENT MODULE
'''
threat_map = get_cvss_scores()
for cve, details in threat_map.items():
    print(f"{cve}: CVSS={details['cvss_score']} | Severity={details['severity_label']} ({details['severity_value']})")

def perform_ofrhm(host_info):
    print(">> [ACTION] Performing OF-RHM on", host_info)

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
        
