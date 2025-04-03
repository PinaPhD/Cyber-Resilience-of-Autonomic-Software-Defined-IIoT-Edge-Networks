#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Mon Mar 17 09:58:25 2025
@Task: ACT Module that creates flows to manipulate the state of the network through the control plane
@author: agrippina mwangi

"""

import random
import pandas as pd
import numpy as np
import requests
import base64
import requests

ONOS_CONTROLLER = "http://10.10.10.43:8181"  #Accessing the primary ONOS SDN Controller
USERNAME = "onos"
PASSWORD = "rocks"

def push_intent_to_onos(app_id, host_id, new_ip, mac):
    intent = {
        "type": "HostToHostIntent",
        "appId": app_id,
        "priority": 200,
        "one": host_id,
        "two": host_id,
        "constraints": [],
        "selector": {
            "criteria": [
                {"type": "ETH_DST", "mac": mac},
                {"type": "IPV4_DST", "ip": new_ip + "/32"}
            ]
        },
        "treatment": {
            "instructions": []
        }
    }

    url = f"{ONOS_CONTROLLER}/onos/v1/intents"

    headers = {
        "Content-Type": "application/json"
    }
    auth = (USERNAME, PASSWORD)

    try:
        response = requests.post(url, headers=headers, json=intent, auth=auth)
        if response.status_code in [200, 201]:
            print(f">> [ONOS] Intent successfully pushed for host {host_id} ({new_ip})")
        else:
            print(f">> [ERROR] Failed to push intent. Status: {response.status_code}, Reason: {response.text}")
    except Exception as e:
        print(f">> [EXCEPTION] Could not reach ONOS: {e}")
