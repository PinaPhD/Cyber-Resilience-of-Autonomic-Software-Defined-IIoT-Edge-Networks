#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 11:00:49 2025
Updated for full GSPN simulation + 4 separate plots and fixed definition for standalone runs
@author: amwangi
"""

import random
import math
import matplotlib.pyplot as plt
import pandas as pd

def simulate_gspn_event_driven_mtd(num_devices, lambda_attack, mu_compromise, 
                                   delta_detection, rho_recovery, t_max):
    safe_count = num_devices
    under_attack_count = 0
    compromised_count = 0

    attack_count = detection_count = compromise_count = recovery_count = 0
    detection_latencies = []
    attack_start_times = {}

    current_time = 0.0
    total_compromised_time = 0.0
    time_series = []

    while current_time < t_max:
        rate_attack = lambda_attack * safe_count
        rate_compromise = mu_compromise * under_attack_count
        rate_detection = delta_detection * under_attack_count
        rate_recovery = rho_recovery * compromised_count
        total_rate = rate_attack + rate_compromise + rate_detection + rate_recovery
        if total_rate == 0:
            break

        time_to_next = random.expovariate(total_rate)
        next_event_time = current_time + time_to_next
        if next_event_time > t_max:
            total_compromised_time += (t_max - current_time) * compromised_count
            current_time = t_max
            break

        r = random.random() * total_rate
        if r < rate_attack:
            event = "attack"
        elif r < rate_attack + rate_compromise:
            event = "compromise"
        elif r < rate_attack + rate_compromise + rate_detection:
            event = "detection"
        else:
            event = "recovery"

        total_compromised_time += (next_event_time - current_time) * compromised_count
        current_time = next_event_time

        if event == "attack":
            attack_count += 1
            safe_count -= 1
            under_attack_count += 1
            attack_start_times[attack_count] = current_time

        elif event == "compromise":
            compromise_count += 1
            under_attack_count -= 1
            compromised_count += 1
            if attack_start_times:
                attack_start_times.popitem()

        elif event == "detection":
            detection_count += 1
            under_attack_count -= 1
            safe_count += 1
            if attack_start_times:
                device_id, start_time = attack_start_times.popitem()
                latency = current_time - start_time
                detection_latencies.append(latency)

        elif event == "recovery":
            recovery_count += 1
            compromised_count -= 1
            safe_count += 1

        frac_compromised = compromised_count / num_devices
        containment_rate = detection_count / attack_count if attack_count > 0 else 0.0
        avg_det_latency = sum(detection_latencies) / len(detection_latencies) if detection_latencies else 0.0
        efficiency_index = 1.0 / (avg_det_latency * containment_rate) if containment_rate > 0 and avg_det_latency > 0 else 0.0
        resilience_index = recovery_count / total_compromised_time if total_compromised_time > 0 else 0.0

        time_series.append((current_time, frac_compromised, containment_rate, efficiency_index, resilience_index))

    intervals = 10
    mtd_counts = ([ (detection_count//2) ] * (intervals//2)) + ([0] * (intervals - intervals//2)) if detection_count > 0 else [0]*intervals
    mean_c = sum(mtd_counts)/len(mtd_counts)
    volatility = sum((c - mean_c)**2 for c in mtd_counts) / len(mtd_counts)

    return time_series, {
        'attacks': attack_count,
        'detections': detection_count,
        'compromises': compromise_count,
        'recoveries': recovery_count,
        'volatility': volatility,
        'avg_detection_latency': avg_det_latency
    }

def run_and_plot_gspn_simulation(num_devices, lambda_attack, mu_compromise, 
                                 delta_detection, rho_recovery, t_max):
    from __main__ import simulate_gspn_event_driven_mtd  # Ensure definition is accessible

    sim_data, totals = simulate_gspn_event_driven_mtd(
        num_devices,
        lambda_attack,
        mu_compromise,
        delta_detection,
        rho_recovery,
        t_max
    )

    print("\n--- GSPN Simulation Summary ---")
    print("Total Attacks:", totals['attacks'])
    print("Contained (MTD) Attacks:", totals['detections'])
    print("Successful Compromises:", totals['compromises'])
    print("Avg Detection Latency:", totals['avg_detection_latency'])
    print("Cyber-Resilience Index (final):", sim_data[-1][4])

    times = [row[0] for row in sim_data]
    compromise_prob = [row[1] for row in sim_data]
    containment_rate = [row[2] for row in sim_data]
    efficiency_index = [row[3] for row in sim_data]
    cri = [row[4] for row in sim_data]

    # Plot 1: Probability of Compromise
    plt.figure(figsize=(10, 4))
    plt.plot(times, compromise_prob, color='red')
    plt.title("Probability of Compromise Over Time")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Fraction of Devices Compromised")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot 2: Containment Rate
    plt.figure(figsize=(10, 4))
    plt.plot(times, containment_rate, color='blue')
    plt.title("Containment Rate Over Time")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Containment Rate")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot 3: Defense Efficiency Index
    plt.figure(figsize=(10, 4))
    plt.plot(times, efficiency_index, color='green')
    plt.title("Defense Efficiency Over Time")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Efficiency Index")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot 4: Cyber-Resilience Index (CRI)
    plt.figure(figsize=(10, 4))
    plt.plot(times, cri, color='purple')
    plt.title("Cyber-Resilience Index Over Time")
    plt.xlabel("Time (seconds)")
    plt.ylabel("CRI")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Example usage:
run_and_plot_gspn_simulation(152, 0.2, 0.05, 0.6, 0.045, 300)
