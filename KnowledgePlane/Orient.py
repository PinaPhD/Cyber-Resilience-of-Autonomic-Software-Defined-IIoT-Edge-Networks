#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Mon Feb 17 09:42:27 2025
    @Task Description: Orient Module that performs anomaly detection and determines the attack severity using the NIST Common Vulnerability Risk Scoring Tool
    @author: Agrippina Mwangi
"""

import requests
from datetime import datetime
import mysql.connector
from Observe import current_network_state   #Loads the current network state as observed real-time

#Reading the current network state
devices, links, hosts, flows, port_stats = current_network_state() 

def get_cvss_scores(cve_ids):
    cvss_cve_map = {}

    for cve_id in cve_ids:
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if 'vulnerabilities' in data and len(data['vulnerabilities']) > 0:
                vuln_data = data['vulnerabilities'][0]['cve']
                metrics = vuln_data.get('metrics', {})

                # Fetch CVSS v3.1 or v3.0 first, otherwise fallback to v2
                cvss_v3 = None
                if 'cvssMetricV31' in metrics:
                    cvss_v3_data = metrics['cvssMetricV31'][0].get('cvssData', {})
                    cvss_v3 = cvss_v3_data.get('baseScore')

                cvss_v3 = cvss_v3 or metrics.get('cvssMetricV3', [{}])[0].get('cvssData', {}).get('baseScore')
                cvss_v2 = metrics.get('cvssMetricV2', [{}])[0].get('cvssData', {}).get('baseScore')

                # Determine CVSS score to use
                cvss_score = cvss_v3 if cvss_v3 is not None else cvss_v2
                cvss_cve_map[cve_id] = cvss_score if cvss_score is not None else "Not Available"
            else:
                cvss_cve_map[cve_id] = "No vulnerability data found"
        else:
            cvss_cve_map[cve_id] = f"HTTP Error {response.status_code}"

    return cvss_cve_map


def multi_log_analysis():
    cve_ids_pool = {}
    
    
    return cve_ids_pool



def insert_threat_to_db(Z, level):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Baarn@2026_',
        database='KNOWLEDGE_BASE'
    )
    cursor = conn.cursor()
    timestamp = datetime.now()
    sql = "INSERT INTO threat_levels (timestamp, z_value, threat_level) VALUES (%s, %s, %s)"
    cursor.execute(sql, (timestamp, Z, level))
    conn.commit()
    cursor.close()
    conn.close()
    
    
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
