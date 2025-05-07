#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
    @Created on Mar 21 13:35:58 2025
    @Task: Designing the GSPN Module that interfaces with the Knowledge Plane of the proposed Software-defined IIoT-Edge network
    @author: Agrippina Mwangi
    @Final Edits Wed May  7 10:59:56 2025
"""


import random
import matplotlib.pyplot as plt

def simulate_gspn_event_driven_mtd(num_devices, lambda_attack, mu_compromise, 
                                   delta_detection, rho_recovery, t_max):
    safe_count = num_devices
    under_attack_count = 0
    compromised_count = 0

    attack_count = detection_count = compromise_count = recovery_count = 0
    detection_latencies = []
    attack_start_times = {}

    disruption_count = 0
    detection_based_recoveries = 0
    prolonged_attack_threshold = 5.0  # seconds
    under_attack_start_times = []

    current_time = 0.0
    total_compromised_time = 0.0
    total_safe_time = 0.0

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
        next_event_time = current_time + time_to_next
        if next_event_time > t_max:
            total_compromised_time += (t_max - current_time) * compromised_count
            total_safe_time += (t_max - current_time) * safe_count
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
        total_safe_time += (next_event_time - current_time) * safe_count
        current_time = next_event_time

        if event == "attack":
            attack_count += 1
            safe_count -= 1
            under_attack_count += 1
            under_attack_start_times.append(current_time)
            attack_start_times[attack_count] = current_time

        elif event == "compromise":
            compromise_count += 1
            under_attack_count -= 1
            compromised_count += 1
            disruption_count += 0.5
            if attack_start_times:
                attack_start_times.popitem()
            if under_attack_start_times:
                under_attack_start_times.pop(0)

        elif event == "detection":
            detection_count += 1
            under_attack_count -= 1
            safe_count += 1
            if attack_start_times:
                device_id, start_time = attack_start_times.popitem()
                latency = current_time - start_time
                detection_latencies.append(latency)
            if under_attack_start_times:
                duration = current_time - under_attack_start_times.pop(0)
                if duration < prolonged_attack_threshold:
                    detection_based_recoveries += 1

        elif event == "recovery":
            recovery_count += 1
            compromised_count -= 1
            safe_count += 1

        frac_compromised = compromised_count / num_devices
        containment_rate = detection_count / attack_count if attack_count > 0 else 0.0
        avg_det_latency = sum(detection_latencies) / len(detection_latencies) if detection_latencies else 0.0
        efficiency_index = avg_det_latency if containment_rate > 0 and avg_det_latency > 0 else 0.0
        epsilon = 1e-6
        cri_index = (recovery_count + detection_based_recoveries) / (
                    recovery_count + detection_based_recoveries + disruption_count + epsilon)

        time_series.append((current_time, frac_compromised, containment_rate, efficiency_index, cri_index))

    return time_series, {
        'attacks': attack_count,
        'detections': detection_count,
        'compromises': compromise_count,
        'recoveries': recovery_count,
        'avg_detection_latency': avg_det_latency
    }


def run_and_plot_gspn_simulation(scenarios, num_devices=152, t_max=300):
    time_series = {}
    compromise_dict = {}
    containment_dict = {}
    efficiency_dict = {}
    cri_dict = {}

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

    def plot_metric(title, ylabel, metric_dict, time_dict):
        plt.figure(figsize=(10, 5))
        for label, values in metric_dict.items():
            plt.plot(time_dict[label], values, label=label)
        plt.title(title, fontsize=20)
        plt.xlabel("Time (seconds)", fontsize=20)
        plt.ylabel(ylabel, fontsize=20)
        plt.grid(True)
        plt.legend(fontsize=14)
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        plt.tight_layout()
        plt.show()

    plot_metric("Probability of System Compromise", "P(compromised)", compromise_dict, time_series)
    plot_metric("Attack Containment Rate (ACR)", "Containment Rate", containment_dict, time_series)
    plot_metric("Defense Activation Efficiency Score", "Efficiency Index", efficiency_dict, time_series)
    plot_metric("System Cyber-Resilience Index (CRI)", "CRI", cri_dict, time_series)

scenarios = [
    {"label": "Passive Recon", "lambda_attack": 0.01, "mu_compromise": 0.001, "delta_detection": 0.85, "rho_recovery": 0.3},
    {"label": "Loud Scan", "lambda_attack": 0.3, "mu_compromise": 0.01, "delta_detection": 0.65, "rho_recovery": 0.25},
    {"label": "Slow APT", "lambda_attack": 0.02, "mu_compromise": 0.01, "delta_detection": 0.25, "rho_recovery": 0.1},
    {"label": "Ransomware", "lambda_attack": 0.7, "mu_compromise": 0.5, "delta_detection": 0.35, "rho_recovery": 0.05},
    {"label": "Insider Leak", "lambda_attack": 0.15, "mu_compromise": 0.08, "delta_detection": 0.15, "rho_recovery": 0.4},
    {"label": "DoS Burst", "lambda_attack": 0.9, "mu_compromise": 0.05, "delta_detection": 0.6, "rho_recovery": 0.15}
]

run_and_plot_gspn_simulation(scenarios)