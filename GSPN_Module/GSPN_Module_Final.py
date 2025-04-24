#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Mar 21 13:35:58 2025
    @Task: Designing the GSPN Module that interfaces with the Knowledge Plane of the proposed Software-defined IIoT-Edge network
    @author: Agrippina Mwangi
"""

import random
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go

# Define GSPN places as variables
places = {
    'norm': 10,               # initial state with 10 tokens
    'detect': 0,
    'detfail': 0,
    'underattack': 0,
    'compromised': 0,
    'defend': 0,
    'partialrestore': 0,
    'fullyrestored': 0
}

time = 0.0
T_MAX = 100.0

# Statistics tracking
stats = {
    't_s1_fired': 0,
    't_s2_fired': 0,
    't_s3_fired': 0,
    't_i3_fired': 0,
    't_i4_fired': 0,
    'compromised_tokens': 0
}

# Define stochastic transition rates (rates for exponential distribution)
rates = {
    't_s1': 0.2,  # compromised -> defend
    't_s2': 0.3,  # defend -> partialrestore
    't_s3': 0.3   # defend -> fullyrestored
}

# Simple event queue simulation for stochastic transitions
events = []  # list of tuples (time, event_type, from_place, to_place)
time_series = []

def schedule_stochastic(event_type, from_place, to_place, rate):
    delay = random.expovariate(rate)
    events.append((time + delay, event_type, from_place, to_place))

def fire_immediate(from_place, to_place):
    if places[from_place] > 0:
        places[from_place] -= 1
        places[to_place] += 1
        return True
    return False

# Initial immediate transitions
def fire_immediate_transitions():
    changed = True
    while changed:
        changed = False
        # norm -> detect
        if fire_immediate('norm', 'detect'):
            changed = True
        # detect -> detfail
        if fire_immediate('detect', 'detfail'):
            changed = True
            # loop back from detfail to norm
            if fire_immediate('detfail', 'norm'):
                changed = True
        # detect -> underattack
        if fire_immediate('detect', 'underattack'):
            stats['t_i3_fired'] += 1
            changed = True
        # underattack -> compromised
        if fire_immediate('underattack', 'compromised'):
            stats['t_i4_fired'] += 1
            stats['compromised_tokens'] += 1
            if places['compromised'] > 0:
                schedule_stochastic('t_s1', 'compromised', 'defend', rates['t_s1'])
            changed = True

# Main simulation loop
while time < T_MAX:
    fire_immediate_transitions()
    time_series.append((time, dict(places)))
    if not events:
        break
    events.sort()  # sort by event time
    next_event = events.pop(0)
    next_time, event_type, from_place, to_place = next_event
    if next_time > T_MAX:
        break
    time = next_time
    if places[from_place] > 0:
        places[from_place] -= 1
        places[to_place] += 1
        if event_type == 't_s1':
            stats['t_s1_fired'] += 1
            if random.random() < 0.5:
                schedule_stochastic('t_s2', 'defend', 'partialrestore', rates['t_s2'])
            else:
                schedule_stochastic('t_s3', 'defend', 'fullyrestored', rates['t_s3'])
        elif event_type == 't_s2':
            stats['t_s2_fired'] += 1
        elif event_type == 't_s3':
            stats['t_s3_fired'] += 1
    time_series.append((time, dict(places)))

# Final output
print("Final Time:", time)
print("Place Counts:", places)
print("Transition Stats:", stats)

# --- Visualization ---
# Create a dataframe for plotting
records = []
for t, place_dict in time_series:
    record = {'time': t}
    record.update(place_dict)
    records.append(record)
df = pd.DataFrame(records)

# Line plot of token counts over time
sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))
for col in places.keys():
    plt.plot(df['time'], df[col], label=col)
plt.title("Token Counts in Each Place Over Time")
plt.xlabel("Time")
plt.ylabel("Number of Tokens")
plt.legend()
plt.tight_layout()
plt.show()

# Sankey diagram
labels = list(places.keys())
source = []
target = []
value = []

# Manually define major flows for simplicity
def add_flow(src, tgt, val):
    if val > 0:
        source.append(labels.index(src))
        target.append(labels.index(tgt))
        value.append(val)

add_flow('norm', 'detect', stats['t_i3_fired'])
add_flow('detect', 'underattack', stats['t_i3_fired'])
add_flow('underattack', 'compromised', stats['t_i4_fired'])
add_flow('compromised', 'defend', stats['t_s1_fired'])
add_flow('defend', 'partialrestore', stats['t_s2_fired'])
add_flow('defend', 'fullyrestored', stats['t_s3_fired'])

fig = go.Figure(data=[go.Sankey(
    node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=labels),
    link=dict(source=source, target=target, value=value))])
fig.update_layout(title_text="Token Flow Sankey Diagram", font_size=10)
fig.show()
