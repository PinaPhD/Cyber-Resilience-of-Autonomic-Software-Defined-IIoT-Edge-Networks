#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Created on Mon Feb 17 09:42:27 2025
    @Task Description: Orient Module that performs anomaly detection and determines the attack severity using the NIST Common Vulnerability Risk Scoring Tool
    @author: Agrippina Mwangi
"""

import requests
from datetime import datetime, timedelta
import mysql.connector
from collections import defaultdict
from Observe import current_network_state   #Loads the current network state as observed real-time

#Reading the current network state
devices, links, hosts, flows, port_stats,snort_logs = current_network_state() 

#Connecting to the knowledge base
DB_HOST = "10.10.10.30"
DB_USER = "pina254"
DB_PASSWORD = "Baarn@2026_"
DB_NAME = "KNOWLEDGE_BASE"


'''
    :Part I:  conduct a multi-log ingestion to observe the threat pattern
    :Param:  Return a cve_id{} that contains 1, ..., m CVE_ids that can be used to determine the threat severity
    :Param:  Perform the log ingestion for logs captured within 5 minutes
'''  

#The multi-log ingestion is computed by assessing the log correlation and ingestion
def multi_log_analysis(time_window_minutes=5):
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
        
        #Define the log analysis time window (Pattern over 5 minutes recommended)
        time_threshold = datetime.now() - timedelta(minutes=time_window_minutes)
        
        #Query the logs within the time window
        query = """
        SELECT src_ip, dest_ip, protocol, classtype, cve_id, timestamp
        FROM snort_logs
        WHERE timestamp >= %s AND cve_id IS NOT NULL
        ORDER BY src_ip, cve_id, timestamp;
        """
        cursor.execute(query, (time_threshold,))
        logs = cursor.fetchall()
        
        '''
            Group logs by source IP and extract CVE IDs
            This strategy reveals targeted attacks from the same source IP attacking multiple destinations 
            and also helps with threat correlation and pattern recognition when the same attacker triggers multiple 
            alerts across different CVEs (hinting at a multi-phase intrusion)
        '''
        
        cve_pool = defaultdict(set)
        for log in logs:
            src_ip = log["src_ip"]
            cve = log["cve_id"]
            if cve:
                cve_pool[src_ip].add(cve)
    
        cursor.close()
        conn.close()
    
        # Flatten CVE pool (unique list)
        unique_cves = set()
        for cves in cve_pool.values():
            unique_cves.update(cves)
    
        return list(unique_cves)
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    
#Based on the cve_ids_pool determine the CVSS from the NIST National Vulnerability Database
def determine_level(Z):
    if Z is None:
        return "none", 0.0
    elif Z < 4.0:
        return "low", 1.0
    elif 4.0 <= Z < 7.0:
        return "medium", 2.0
    elif 7.0 <= Z <= 9.0:
        return "high", 3.0
    else:
        return "critical", 4.0

#Based on the resulting CVSS Obtained, the threat severity level, Z, determines what the DEFENSE Module should do at time,t.   
def get_cvss_scores():
    cve_ids = multi_log_analysis(time_window_minutes=5)
    cvss_cve_map = {}

    for cve_id in cve_ids:
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if 'vulnerabilities' in data and len(data['vulnerabilities']) > 0:
                vuln_data = data['vulnerabilities'][0]['cve']
                metrics = vuln_data.get('metrics', {})

                # Try CVSS v3.1, then v3.0, then fallback to v2
                cvss_v3 = None
                if 'cvssMetricV31' in metrics:
                    cvss_v3 = metrics['cvssMetricV31'][0].get('cvssData', {}).get('baseScore')
                if cvss_v3 is None and 'cvssMetricV3' in metrics:
                    cvss_v3 = metrics['cvssMetricV3'][0].get('cvssData', {}).get('baseScore')

                cvss_v2 = metrics.get('cvssMetricV2', [{}])[0].get('cvssData', {}).get('baseScore')

                cvss_score = cvss_v3 if cvss_v3 is not None else cvss_v2
                severity_label, severity_value = determine_level(cvss_score)

                cvss_cve_map[cve_id] = {
                    "cvss_score": cvss_score if cvss_score is not None else "No Threat Detected",
                    "severity_label": severity_label,
                    "severity_value": severity_value
                }

            else:
                cvss_cve_map[cve_id] = {
                    "cvss_score": "No vulnerability data found",
                    "severity_label": "unknown",
                    "severity_value": 0.0
                }

        else:
            cvss_cve_map[cve_id] = {
                "cvss_score": f"HTTP Error {response.status_code}",
                "severity_label": "unknown",
                "severity_value": 0.0
            }

    return cvss_cve_map
