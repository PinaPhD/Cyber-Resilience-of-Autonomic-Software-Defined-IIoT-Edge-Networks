#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 10:07:51 2025
@Task: Mapping the SNORT Alerts to CVSS Scores. Query the NIST National Vulnerability Database (NVD)'s API with the CVE identifiers (already defined in the SNORT logs)'
@author: agrippina mwangi 
"""

import requests

def get_cvss_score(cve, api_key):
    # Base URL for the NVD API endpoint
    url = f"https://api.nist.gov/vuln/data/cve/{cve}"
    
    # Headers with your API key
    headers = {
        'apiKey': api_key
    }

    # Send the GET request with the headers
    response = requests.get(url, headers=headers)
    
    # Check the status code to ensure the request is successful
    if response.status_code == 200:
        try:
            # Parse the JSON response to extract the CVSS score
            cve_data = response.json()
            cvss_score = cve_data['result']['CVE_Items'][0]['impact']['baseMetricV3']['cvssV3']['baseScore']
            return cvss_score
        except KeyError:
            print("Error: CVSS score not found in the response")
            return None
    else:
        print(f"Error: Unable to fetch CVE data for {cve}. Status Code: {response.status_code}")
        return None

# Replace with your actual API key
api_key = 'd0d03cb1-6484-43d1-b9ab-6383634fdcd2 '

# Example CVE to query
cve = 'CVE-2021-3156'

# Get the CVSS score for the CVE
cvss_score = get_cvss_score(cve, api_key)

if cvss_score is not None:
    print(f"The CVSS score for {cve} is: {cvss_score}")
else:
    print("Failed to retrieve CVSS score")
