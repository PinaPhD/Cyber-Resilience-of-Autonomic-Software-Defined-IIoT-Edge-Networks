#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Tue Apr 15 22:53:31 2025
    @Task: GSPN Module
    @author: agrippina mwangi
"""


import argparse
import random, math, csv, itertools

# Parse command-line arguments for transition rates and optional sweeps
parser = argparse.ArgumentParser(description="Simulate a cyber-resilient system (GSPN model) over 24h.")
parser.add_argument('--lambda_attack', nargs='+', type=float, default=[0.5],
                    help="Attack arrival rate λ_attack (per hour). Can provide multiple values for sweep.")
parser.add_argument('--lambda_detect', nargs='+', type=float, default=[0.5],
                    help="IDS detection rate λ_detect (per hour). Can provide multiple values for sweep.")
parser.add_argument('--lambda_comp', nargs='+', type=float, default=[0.5],
                    help="Attacker compromise rate λ_comp (per hour). Can provide multiple values for sweep.")
parser.add_argument('--lambda_recover', nargs='+', type=float, default=[0.5],
                    help="Compromise recovery rate λ_recover (per hour). Can provide multiple values for sweep.")
parser.add_argument('--lambda_shuffle', nargs='+', type=float, default=[0.5],
                    help="MTD IP/MAC shuffle rate λ_shuffle (per hour, only active in Safe state). Multiple values allowed.")
parser.add_argument('--runs', type=int, default=1000, 
                    help="Number of simulation runs to perform (default 1000).")
parser.add_argument('--output', type=str, default="simulation_results.csv", 
                    help="Output CSV file name for results.")
args = parser.parse_args()

# Prepare all combinations of parameter values (for sweeps if multiple values provided)
param_combinations = list(itertools.product(args.lambda_attack, args.lambda_detect, 
                                           args.lambda_comp, args.lambda_recover, args.lambda_shuffle))
multiple_scenarios = len(param_combinations) > 1

# Open CSV for writing results
with open(args.output, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header:
    header = []
    if multiple_scenarios:
        header += ["lambda_attack", "lambda_detect", "lambda_comp", "lambda_recover", "lambda_shuffle"]
    header += ["ProbCompromise", "DefenseEff", "AttackSurfaceVolatility", "CRI"]
    writer.writerow(header)
    
    # Run simulations for each parameter combination
    for (lamA, lamD, lamC, lamR, lamS) in param_combinations:
        for run in range(args.runs):
            # Simulation of one 24h run
            time = 0.0
            state = "Safe"
            compromised = False
            attacks_count = detection_count = compromise_count = recover_count = 0
            shuffle_times = []
            # Schedule first attack and shuffle
            next_attack_time = (random.expovariate(lamA) if lamA > 0 else math.inf)
            next_shuffle_time = (random.expovariate(lamS) if lamS > 0 else math.inf)
            # Timers for detection/compromise (active during an attack) and recovery (during compromised)
            det_time = comp_time = rec_time = math.inf
            
            # Event loop for 24h
            while time < 24.0:
                if state == "Safe":
                    # Determine next event in Safe state
                    next_event_time = min(next_attack_time, next_shuffle_time)
                    if next_event_time == math.inf or next_event_time > 24.0:
                        break  # no more events within 24h
                    time = next_event_time
                    if next_attack_time <= next_shuffle_time:
                        # Attack starts
                        state = "UnderAttack"
                        attacks_count += 1
                        # Pause shuffling during attack
                        next_shuffle_time = math.inf  
                        # Schedule detection and compromise attempts from this point
                        det_time = time + (random.expovariate(lamD) if lamD > 0 else math.inf)
                        comp_time = time + (random.expovariate(lamC) if lamC > 0 else math.inf)
                    else:
                        # Shuffle event occurs
                        shuffle_times.append(time)
                        # Schedule the next shuffle
                        next_shuffle_time = time + (random.expovariate(lamS) if lamS > 0 else math.inf)
                    # Loop back for next event
                    continue
                
                if state == "UnderAttack":
                    # Determine outcome of the ongoing attack (detection or compromise)
                    next_event_time = min(det_time, comp_time)
                    if next_event_time == math.inf or next_event_time > 24.0:
                        break  # attack outcome happens beyond 24h, stop at horizon
                    time = next_event_time
                    if det_time <= comp_time:
                        # Attack detected before compromise
                        detection_count += 1
                        state = "Safe"
                        # Schedule next attack and shuffle after this detection
                        next_attack_time = time + (random.expovariate(lamA) if lamA > 0 else math.inf)
                        next_shuffle_time = time + (random.expovariate(lamS) if lamS > 0 else math.inf)
                    else:
                        # Attack succeeds (system compromised)
                        compromise_count += 1
                        compromised = True
                        state = "Compromised"
                        # Schedule recovery after compromise
                        rec_time = time + (random.expovariate(lamR) if lamR > 0 else math.inf)
                    # Reset attack-specific timers
                    det_time = comp_time = math.inf
                    continue
                
                if state == "Compromised":
                    # Wait for recovery
                    next_event_time = rec_time
                    if next_event_time == math.inf or next_event_time > 24.0:
                        break  # recovery happens after 24h or not at all within horizon
                    time = next_event_time
                    recover_count += 1
                    state = "Safe"
                    # System recovered, schedule next attack and shuffle
                    next_attack_time = time + (random.expovariate(lamA) if lamA > 0 else math.inf)
                    next_shuffle_time = time + (random.expovariate(lamS) if lamS > 0 else math.inf)
                    rec_time = math.inf
                    continue
            
            # Compute metrics for this run
            prob_compromise = 1.0 if compromised else 0.0
            defense_eff = (detection_count / attacks_count) if attacks_count > 0 else 0.0
            # Compute variance of shuffle intervals (if at least two shuffles occurred)
            intervals = [shuffle_times[i] - shuffle_times[i-1] for i in range(1, len(shuffle_times))]
            if len(intervals) > 1:
                mean_int = sum(intervals) / len(intervals)
                var_interval = sum((x - mean_int) ** 2 for x in intervals) / len(intervals)
            else:
                var_interval = 0.0
            CRI = recover_count / (compromise_count + 1e-9)
            
            # Write the row (include param values if multiple scenarios)
            row = []
            if multiple_scenarios:
                row += [lamA, lamD, lamC, lamR, lamS]
            row += [prob_compromise, defense_eff, var_interval, CRI]
            writer.writerow(row)
