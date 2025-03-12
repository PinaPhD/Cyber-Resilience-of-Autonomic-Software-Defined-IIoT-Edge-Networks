#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 13:35:58 2025

@author: Agrippina Mwangi
"""

#Importing relevant helper functions
import random
import requests
import time


from Observe import current_network_state   #Loads the current network state as observed real-time


devices, links, hosts, flows, port_stats = current_network_state() 


