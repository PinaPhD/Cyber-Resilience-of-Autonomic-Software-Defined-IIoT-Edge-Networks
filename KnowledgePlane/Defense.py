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


'''
    Initialize section ---> In the Initialize_mtd() function
        :Param - subnet pools, K, for different regions
        :Param - Assign each host an IP from the tuple
        :Param - configure micro-segmentation "Intents" --- Linking to the ACT Module
        :Param - Compute the Risk Score (Rh)
'''

#Defining host dictionary structured as a tuple comprising (rIP, vIP1, vIP2)
switch_host_info = initialize_mtd()

devices, links, hosts, flows, port_stats = current_network_state() 

'''
STEP 3/4: Read CVSS from threat intelligence sources and determining the threat severity (Z)
--- ORIENT MODULE
'''

Z=9

if Z is None:
    print("No threat detected")
if Z < 4.0:
    print("Recon attack detected")
elif 4.0 <= Z < 7.0:
    print("Medium threat level")
elif 7.0<= Z <= 9.0:
    print("Hight threat level")    
else:
    print("Critical")




'''
STEP 5: Perform random host mutation for targetted regions
--- DEFENSE MODULE
'''

