# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 11:35:30 2025

@author: Mwang002
"""

from snakes.nets import *
from snakes.nets import PetriNet, Place, Transition, Value, Substitution
import random


# Create the net
gspn = PetriNet('MTD_GSPN')

# Define Places
gspn.add_place(Place('P_norm', [1]))
gspn.add_place(Place('P_recon'))
gspn.add_place(Place('P_cross'))
gspn.add_place(Place('P_ddos'))
gspn.add_place(Place('P_mtd'))
gspn.add_place(Place('P_recp'))
gspn.add_place(Place('P_recf'))

# Define Transitions
gspn.add_transition(Transition('t_susp'))
gspn.add_transition(Transition('t_fail'))
gspn.add_transition(Transition('t_suspect'))
gspn.add_transition(Transition('t_mtdd'))
gspn.add_transition(Transition('t_mtdc'))
gspn.add_transition(Transition('t_mtdr'))
gspn.add_transition(Transition('t_recp'))
gspn.add_transition(Transition('t_recf'))

# Add Arcs (example for t_susp leading to different attack states based on external threat input)
gspn.add_input('P_norm', 't_susp', Value(1))
gspn.add_output('P_recon', 't_susp', Value(1))
gspn.add_output('P_cross', 't_susp', Value(1))
gspn.add_output('P_ddos', 't_susp', Value(1))

# MTD responses
for attack_place, transition in [('P_ddos', 't_mtdd'), ('P_cross', 't_mtdc'), ('P_recon', 't_mtdr')]:
    gspn.add_input(attack_place, transition, Value(1))
    gspn.add_output('P_mtd', transition, Value(1))

# Recovery from MTD
for transition, target in [('t_recp', 'P_recp'), ('t_recf', 'P_recf')]:
    gspn.add_input('P_mtd', transition, Value(1))
    gspn.add_output(target, transition, Value(1))

# Simple simulation function
def simulate_step(threat_level):
    print("\n--- Simulation Step ---")
    if gspn.place('P_norm').tokens:
        gspn.transition('t_susp').fire(Substitution())
        print(f"Threat detected: {threat_level}, transition 't_susp' fired")

        if threat_level == 'Low':
            gspn.place('P_recon').add(1)
        elif threat_level in ['Medium', 'High']:
            gspn.place('P_cross').add(1)
        elif threat_level == 'Critical':
            gspn.place('P_ddos').add(1)

    # Fire MTD response if any attack place has tokens
    for place, transition in [('P_ddos', 't_mtdd'), ('P_cross', 't_mtdc'), ('P_recon', 't_mtdr')]:
        if gspn.place(place).tokens:
            gspn.transition(transition).fire(Substitution())
            print(f"MTD triggered: {transition} fired")

    # Random recovery path
    if gspn.place('P_mtd').tokens:
        recovery = random.choice(['t_recp', 't_recf'])
        gspn.transition(recovery).fire(Substitution())
        print(f"Recovery phase: {recovery} fired")

    # Print markings
    for place in gspn.place():
        print(f"{place.name}: {place.tokens}")

# Example simulation run
threat_scenarios = ['Low', 'Medium', 'High', 'Critical', 'None']
for _ in range(5):
    simulate_step(random.choice(threat_scenarios))
