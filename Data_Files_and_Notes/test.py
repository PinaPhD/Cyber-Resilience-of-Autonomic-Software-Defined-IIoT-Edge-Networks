#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 14:35:25 2025

@author: amwangi
"""

from mininet.net import Mininet
net = Mininet()
r1 = net.get('r1')
print(r1.IP())  # Get current IP of host r1
r1.setIP('192.168.16.31', intf='h1-eth0')  # Change IP dynamically
print(r1.IP())  # Verify new IP
