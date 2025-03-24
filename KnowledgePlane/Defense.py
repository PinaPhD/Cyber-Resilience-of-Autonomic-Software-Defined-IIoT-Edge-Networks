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
devices, links, hosts, flows, port_stats = current_network_state() 

#Reading the knowledge base for SNORT Logs stored in the previous 1 minute:
cve_id = ["CVE-2022-22965"]

'''
STEP 3/4: Read CVSS from threat intelligence sources and determining the threat severity (Z)
--- ORIENT MODULE
'''
Z = get_cvss_scores(cve_id)





'''
STEP 5: Perform random host mutation for targetted regions
--- DEFENSE MODULE
'''

