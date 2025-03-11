# -*- coding: utf-8 -*-
"""

    Created on Tue Mar 11 10:55:49 2025
    @Task: Cyber resilience? How do we measure it? --- A case of Generalized Stochastic PetriNets system model
    @author: Agrippina Mwangi

"""

import pypn
import random

# Define places (states in the system)
places = {
    "norm": pypn.Place("P_norm"),      # Normal state
    "recon": pypn.Place("P_recon"),    # Recon state
    "cross": pypn.Place("P_cross"),    # Cross state
    "ddos": pypn.Place("P_ddos"),      # DDoS state
    "mtd": pypn.Place("P_mtd"),        # MTD state (Mitigation)
    "recp": pypn.Place("P_recp"),      # Partial recovery state
    "recf": pypn.Place("P_recf")       # Full recovery state
}

# Define transitions (actions or events in the system)
transitions = {
    "susp": pypn.Transition("t_susp"),          # Suspicion of a threat
    "fail": pypn.Transition("t_fail"),          # Failure to transition
    "suspect": pypn.Transition("t_suspect"),    # Threat categorization
    "mtdd": pypn.Transition("t_mtdd"),          # Mitigation DDOS
    "mtdc": pypn.Transition("t_mtdc"),          # Mitigation Cross
    "mtdr": pypn.Transition("t_mtdr"),          # Mitigation Recon
    "recp": pypn.Transition("t_recp"),          # Partial recovery
    "recf": pypn.Transition("t_recf")           # Full recovery
}

# Define firing rates (exponentially distributed)
firing_rates = {
    "recon": random.expovariate(1),   # Recon transition rate
    "cross": random.expovariate(1),   # Cross transition rate
    "ddos": random.expovariate(1),    # DDoS transition rate
    "recp": random.expovariate(1),    # Partial recovery transition rate
    "recf": random.expovariate(1)     # Full recovery transition rate
}

# Connect transitions to places
transitions["susp"].add_input(places["norm"])
transitions["susp"].add_output(places["recon"], rate=firing_rates["recon"])
transitions["susp"].add_output(places["cross"], rate=firing_rates["cross"])
transitions["susp"].add_output(places["ddos"], rate=firing_rates["ddos"])

# Connecting failure transition
transitions["fail"].add_input(places["recon"])
transitions["fail"].add_input(places["cross"])
transitions["fail"].add_input(places["ddos"])
transitions["fail"].add_output(places["mtd"])

# Connecting mitigation transitions
transitions["mtdd"].add_input(places["ddos"])
transitions["mtdd"].add_output(places["mtd"])
transitions["mtdc"].add_input(places["cross"])
transitions["mtdc"].add_output(places["mtd"])
transitions["mtdr"].add_input(places["recon"])
transitions["mtdr"].add_output(places["mtd"])

# Recovery transitions
transitions["recp"].add_input(places["mtd"])
transitions["recp"].add_output(places["recp"], rate=firing_rates["recp"])
transitions["recf"].add_input(places["mtd"])
transitions["recf"].add_output(places["recf"], rate=firing_rates["recf"])

# Place and transition initialization for the model
net = pypn.Net()

# Add places and transitions to the Petri net
for place in places.values():
    net.add_place(place)
for transition in transitions.values():
    net.add_transition(transition)

# Specify initial marking
initial_marking = {
    places["norm"]: 1  # Network starts in normal state
}

# Set initial marking in the net
net.set_initial_marking(initial_marking)

# Print the Petri net
net.visualize()

# Run simulation to evaluate the system's behavior
results = net.simulate(steps=100)

# Output the results (e.g., system states, firing rates)
print("Simulation Results:", results)
