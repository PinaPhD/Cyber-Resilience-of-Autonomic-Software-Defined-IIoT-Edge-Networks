#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Mar 21 13:35:58 2025
    @Task: Designing the GSPN Module that interfaces with the Knowledge Plane of the proposed Software-defined IIoT-Edge network
    @author: Agrippina Mwangi
"""

import random
import matplotlib.pyplot as plt

# GSPN simulation function
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
        
        time_to_next = max(0.01, random.expovariate(total_rate))
        #time_to_next = random.expovariate(total_rate)
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
        efficiency_index = (1.0 / avg_det_latency) * containment_rate if containment_rate > 0 and avg_det_latency > 0 else 0.0
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


def run_and_plot_gspn_simulation(scenarios, num_devices=152, t_max=300):
    # Storage for time series and metrics per scenario
    time_series = {}
    compromise_dict = {}
    containment_dict = {}
    efficiency_dict = {}
    cri_dict = {}

    # Run simulations
    for scenario in scenarios:
        label = scenario["label"]
        sim_data, _ = simulate_gspn_event_driven_mtd(
            num_devices,
            scenario["lambda_attack"],
            scenario["mu_compromise"],
            scenario["delta_detection"],
            scenario["rho_recovery"],
            t_max
        )
        
        time_series[label] = [point[0] for point in sim_data]


        compromise_dict[label] = [point[1] for point in sim_data]
        containment_dict[label] = [point[2] for point in sim_data]
        efficiency_dict[label] = [point[3] for point in sim_data]
        cri_dict[label] = [point[4] for point in sim_data]

    

    # Plotting function
    def plot_metric(title, ylabel, metric_dict, time_dict):
        plt.figure(figsize=(12, 5))
        for label, values in metric_dict.items():
            plt.plot(time_dict[label], values, label=label)
        plt.title(title, fontsize=16)
        plt.xlabel("Time (seconds)", fontsize=16)
        plt.ylabel(ylabel, fontsize=16)
        plt.grid(True)
        plt.legend(fontsize=13)
        plt.tight_layout()
        plt.show()


    # Generate all 4 plots
    plot_metric("Probability of System Compromise", "P(compromised)", compromise_dict, time_series)
    plot_metric("Attack Containment Rate (ACR)", "Containment Rate [0.0-1.0]", containment_dict, time_series)
    plot_metric("Defense Activation Efficiency Score","Efficiency Index", efficiency_dict, time_series)
    plot_metric("Cyber-Resilience Index (CRI) Over Time", "CRI", cri_dict, time_series)


# === Define GSPN Scenarios (from your LaTeX table) ===
scenarios = [
    {"label": "Baseline", "lambda_attack": 0.2,  "mu_compromise": 0.05,   "delta_detection": 0.5,  "rho_recovery": 0.1374},
    {"label": "Case 1",       "lambda_attack": 0.005, "mu_compromise": 0.0001, "delta_detection": 0.6,  "rho_recovery": 0.00647},
    {"label": "Case 2",       "lambda_attack": 0.01,  "mu_compromise": 0.0025, "delta_detection": 0.65, "rho_recovery": 0.3135},
    {"label": "Case 3",       "lambda_attack": 0.35,  "mu_compromise": 0.0045, "delta_detection": 0.7,  "rho_recovery": 0.5904},
    {"label": "Case 4",       "lambda_attack": 0.5,   "mu_compromise": 0.015,  "delta_detection": 0.75, "rho_recovery": 0.1123},
    {"label": "Case 5",       "lambda_attack": 0.65,  "mu_compromise": 0.035,  "delta_detection": 0.8,  "rho_recovery": 0.4598},
]

# === Run Simulations and Plot All Metrics ===
run_and_plot_gspn_simulation(scenarios)
