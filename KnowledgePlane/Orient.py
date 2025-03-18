#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Mon Feb 17 09:42:27 2025
    @Task Description: Orient Module that performs anomaly detection and determines the attack severity using the NIST Common Vulnerability Risk Scoring Tool
    @author: Agrippina Mwangi
"""

import requests
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





