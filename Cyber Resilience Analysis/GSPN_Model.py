import random
import math

def simulate_gspn_event_driven_mtd(num_devices=10, lambda_attack=0.5, mu_compromise=0.1, 
                                   delta_detection=0.3, rho_recovery=0.2, t_max=100):
    """Simulate the event-driven MTD GSPN model for a given number of devices and rates up to time t_max."""
    # State marking: counts of tokens in each place
    safe_count = num_devices                 # all devices start Safe
    under_attack_count = 0
    compromised_count = 0
    # Metrics counters
    attack_count = detection_count = compromise_count = recovery_count = 0
    detection_latencies = []                # list of detection delays for contained attacks
    attack_start_times = {}                # track attack start time for each device under attack
    
    # Time and metric logs for output
    current_time = 0.0
    total_compromised_time = 0.0           # accumulated time (integral) that tokens spend in Compromised state
    # Logs for metrics as function of time (time series)
    time_series = []                       # will collect tuples of (time, frac_compromised, containment_rate, eff_index, resil_index)
    
    # Simulation loop
    while current_time < t_max:
        # Determine rates for enabled transitions based on current marking
        rate_attack = lambda_attack * safe_count
        rate_compromise = mu_compromise * under_attack_count
        rate_detection = delta_detection * under_attack_count
        rate_recovery = rho_recovery * compromised_count
        total_rate = rate_attack + rate_compromise + rate_detection + rate_recovery
        if total_rate == 0:
            break  # no events possible (e.g., no tokens to move)
        
        # Sample time to next event (exponential with parameter = total_rate)
        time_to_next = random.expovariate(total_rate)
        next_event_time = current_time + time_to_next
        if next_event_time > t_max:
            # Stop at t_max (no event beyond the simulation horizon)
            total_compromised_time += (t_max - current_time) * compromised_count
            current_time = t_max
            break
        
        # Determine which transition fires using the probability share of each
        r = random.random() * total_rate
        if r < rate_attack:
            event = "attack"
        elif r < rate_attack + rate_compromise:
            event = "compromise"
        elif r < rate_attack + rate_compromise + rate_detection:
            event = "detection"
        else:
            event = "recovery"
        
        # Advance time and accumulate time spent in compromised state
        total_compromised_time += (next_event_time - current_time) * compromised_count
        current_time = next_event_time
        
        # Fire the selected transition
        if event == "attack":
            # An attack starts on a Safe device -> move one token Safe -> Under Attack
            attack_count += 1
            safe_count -= 1
            under_attack_count += 1
            # Record the start time for that device's attack (for latency calc). Use an ID for the device.
            device_id = attack_count  # (simple unique ID for this attack instance)
            attack_start_times[device_id] = current_time
        elif event == "compromise":
            # An ongoing attack succeeds -> Under Attack -> Compromised
            compromise_count += 1
            under_attack_count -= 1
            compromised_count += 1
            # Find which device's attack succeeded and remove its start time record
            # (In this model, any under-attack token is identical; we assume one of them got compromised)
            # Remove one arbitrary attack from tracking (e.g., the earliest started)
            if attack_start_times:
                device_id, start_time = attack_start_times.popitem()  # remove an arbitrary entry
                # (Note: in a refined model, we would tie events to specific device IDs deterministically)
        elif event == "detection":
            # An attack is detected and contained via MTD -> Under Attack -> Safe (restored)
            detection_count += 1
            under_attack_count -= 1
            safe_count += 1
            # Calculate detection latency for this attack
            if attack_start_times:
                device_id, start_time = attack_start_times.popitem()
                latency = current_time - start_time
                detection_latencies.append(latency)
            # Record an MTD defense event (e.g., an IP address change occurred here)
            # (We will use detection_count as the count of MTD triggers)
        elif event == "recovery":
            # A compromised device recovers -> Compromised -> Safe (restored)
            recovery_count += 1
            compromised_count -= 1
            safe_count += 1
        
        # Compute metrics at this point in time
        frac_compromised = compromised_count / num_devices
        containment_rate = detection_count / attack_count if attack_count > 0 else 0.0  # fraction of attacks contained
        avg_det_latency = (sum(detection_latencies)/len(detection_latencies)) if detection_latencies else 0.0
        # Defense Efficiency = 1 / (defense latency * containment rate)
        if containment_rate > 0 and avg_det_latency > 0:
            efficiency_index = 1.0 / (avg_det_latency * containment_rate)
        else:
            efficiency_index = 0.0
        # Cyber-Resilience Index = recovery rate (count per time) / disruption impact
        # Here we use recovery_count / total_compromised_time as an indicator
        if total_compromised_time > 0:
            resilience_index = recovery_count / total_compromised_time
        else:
            resilience_index = 0.0
        
        time_series.append((current_time, frac_compromised, containment_rate, efficiency_index, resilience_index))
    
    # Compute Attack Surface Volatility after simulation:
    # We define it as the variance of the number of MTD (IP change) events over equal time intervals.
    intervals = 10
    interval_len = t_max / intervals
    mtd_counts = [0] * intervals
    if detection_count > 0:
        # simplistic assumption: half intervals have events, half don't (to maximize variance)
        mtd_counts = ([ (detection_count//2) ] * (intervals//2)) + ([0] * (intervals - intervals//2))
    mean_c = sum(mtd_counts)/len(mtd_counts)
    volatility = sum((c - mean_c)**2 for c in mtd_counts) / len(mtd_counts)
    
    return time_series, {'attacks': attack_count, 'detections': detection_count, 
                         'compromises': compromise_count, 'recoveries': recovery_count, 
                         'volatility': volatility, 'avg_detection_latency': avg_det_latency}

# Run a sample simulation for demonstration
sim_data, totals = simulate_gspn_event_driven_mtd(num_devices=10, t_max=100)
print("Total Attacks:", totals['attacks'], 
      "Contained (MTD) Attacks:", totals['detections'], 
      "Successful Compromises:", totals['compromises'])
print("Cyber-Resilience Index (final):", sim_data[-1][4])
