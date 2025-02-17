#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 09:42:27 2025

@author: amwangi
"""

from Observe import current_network_state   #Loads the current network state as observed real-time


devices, links, hosts, flows, port_stats = current_network_state() 