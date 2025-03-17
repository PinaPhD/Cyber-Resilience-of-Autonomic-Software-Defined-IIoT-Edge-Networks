#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Mon Feb 17 09:42:27 2025
    @Task Description: Orient Module that performs anomaly detection and determines the attack severity using the NIST Common Vulnerability Risk Scoring Tool
    @author: Agrippina Mwangi
"""

import requests
from Observe import current_network_state   #Loads the current network state as observed real-time


devices, links, hosts, flows, port_stats = current_network_state() 

def get_cvss_score(cve_id):
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
            
            if cvss_score is not None:
                severity = determine_severity(cvss_score)
                return f"CVE ID: {cve_id}\nCVSS Score: {cvss_score}\nSeverity Level: {severity}"
            else:
                return f"CVE ID: {cve_id}\nCVSS Score: Not Available"
        else:
            return f"CVE ID: {cve_id}\nNo vulnerability data found in the response."
    else:
        return f"Failed to retrieve data: HTTP {response.status_code}"

def determine_severity(score):
    if score >= 9.0:
        return "Critical"
    elif score >= 7.0:
        return "High"
    elif score >= 4.0:
        return "Medium"
    else:
        return "Low"

# Example usage

cve_id = "CVE-2022-20685"
print(get_cvss_score(cve_id))
