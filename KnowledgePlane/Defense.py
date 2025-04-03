#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Fri Feb 21 13:35:58 2025
    @Task: Event triggered moving target defense module running at the Knowledge Plane of the Software-defined IIoT-Edge network
    @author: Agrippina Mwangi
"""

import random
import requests
from ipaddress import ip_network, ip_address
from Initialize import initialize_mtd
from Initialize import dhcp_network_plan
from Observe import current_network_state   #Network Health - OODA framework
from Orient import get_cvss_scores
from datetime import datetime, timedelta
import mysql.connector

'''
    Initialize section ---> In the Initialize_mtd() function
        :Param - subnet pools, K, for different regions
        :Param - Assign each host an IP from the tuple
        :Param - configure micro-segmentation "Intents" --- Linking to the ACT Module
        :Param - Compute the Risk Score (Rh)
'''

#Connecting to the knowledge base
DB_HOST = "10.10.10.30"
DB_USER = "pina254"
DB_PASSWORD = "Baarn@2026_"
DB_NAME = "KNOWLEDGE_BASE"

# ONOS controller details
ONOS_CONTROLLER = "http://10.10.10.43:8181"
USERNAME = "onos"
PASSWORD = "rocks"

switch_host_info = initialize_mtd()  #Defining host dictionary structured as a tuple comprising (rIP, vIP1, vIP2)
_, _, host_group_mapping = dhcp_network_plan() #To access subnet pools and host group mapping
devices, links, hosts, flows, port_stats, snort_logs = current_network_state() #Reading the current network state

#Store all the assigned IPs to avoid reusing them
assigned_ips = set(switch_host_info[0].tolist() + switch_host_info[1].tolist() + switch_host_info[2].tolist())

'''
STEP 3/4: Read CVSS from threat intelligence sources and determining the threat severity (Z)
--- ORIENT MODULE
'''

threat_map = get_cvss_scores()
for cve, details in threat_map.items():
    print(f"{cve}: CVSS={details['cvss_score']} | Severity={details['severity_label']} ({details['severity_value']})")

def log_mutation_event_to_mysql(host_id, rIP, new_vIP, vMAC, severity_level):
    #connect to the MYSQL server running on port 
    conn = None
    cursor = None

    try:
        # Establish database connection
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        query = """
        INSERT INTO rhm_mutation_log
        (host_id, real_ip, mutated_vip, mac_address, severity, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        values = (host_id, rIP, new_vIP, vMAC, severity_level, timestamp)

        cursor.execute(query, values)
        conn.commit()

        print(f">> [LOG] Mutation event stored in MySQL for {host_id}")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f">> [ERROR] Failed to log to MySQL: {err}")
        
def perform_ofrhm(host_info, severity_level=None):
    mutated_hosts = []
    print(">> [ACTION] Performing OF-RHM with dual vIPs on", host_info)

    for index, row in host_info.iterrows():
        host_name = row['host_names']
        rIP = row[0]
        vIP1 = row[1]
        vIP2 = row[2]

        region = next((reg for reg, hosts in host_group_mapping.items() if host_name in hosts), None)

        if not region:
            print(f">> [OF-RHM] Region not found for host {host_name}. Skipping.")
            continue

        subnet_info = dhcp_network_plan()[0][region]
        ip_range_start = ip_address(subnet_info["rangeStart"])
        ip_range_end = ip_address(subnet_info["rangeEnd"])
        subnet_ips = [str(ip) for ip in ip_network(subnet_info["subnet"]).hosts()
                      if ip_range_start <= ip <= ip_range_end]

        # Strictly apply: I_K = { x ∈ I | x ∈ pool(K) ∧ x ∉ { rIP_i ∀i ∈ H } }
        excluded_ips = assigned_ips.union({rIP})  # Also exclude rIP
        available_ips = [ip for ip in subnet_ips if ip not in excluded_ips]

        if not available_ips:
            print(f">> [OF-RHM] No available IPs in pool for host {host_name}. Mutation skipped.")
            continue

        new_vIP = random.choice(available_ips)
        assigned_ips.add(new_vIP)  # Already present
        assigned_ips.add(rIP)      # Add real IP explicitly to exclusion pool


        # Let's assume vIP1 is active and gets replaced first
        old_vIP = vIP1
        vIP1 = new_vIP

        print(f">> [OF-RHM] Host {host_name} mutated: vIP1 {old_vIP} → {new_vIP} (rIP remains: {rIP})")

        log_mutation_event_to_mysql(
            host_id=host_name,
            rIP=rIP,
            new_vIP=new_vIP,
            vMAC=row['host_id'].split('/')[0],
            severity_level=severity_level
        )

        mutated_hosts.append({
            "host": host_name,
            "rIP": rIP,
            "new_vIP1": vIP1,
            "vIP2": vIP2,
            "replaced": old_vIP
        })

    return mutated_hosts

'''
     For the functions notify_admin() and log_incident() these may be updated depending
     on the approach used by the organization (email, ticketing system at the NOC center) etc...
'''
def notify_admin(cve_id, severity_label):
    print(f">> [NOTIFY] Admin notified of {severity_label.upper()} threat: {cve_id}")

def log_incident(cve_id, severity_label):
    print(f">> [LOG] Incident logged: {cve_id} ({severity_label})")
    
'''
    Other defense module actions are:
'''

def isolate_host(host_info):
    print(">> [ACTION] Isolating host", host_info)

def block_source_ip(host_info):
    print(">> [ACTION] Blocking source IP", host_info)

def increase_flow_timeout():
    print(">> [ACTION] Flow timeout increased.")

def increase_monitoring_flow():
    print(">> [ACTION] Monitoring frequency increased on affected flows.")

def log_forensics(cve_id):
    print(f">> [LOG] {cve_id} flagged for manual review/forensics.")

def is_network_degraded(r=2): 
    """
    Determines the current network health based on a rolling window of 'r' minutes.
    Network health states:
        - 'idle': Very low traffic, no errors or drops.
        - 'stable': Moderate traffic, acceptable error/drop rates.
        - 'busy': High traffic or noticeable errors/drops.
        - 'unknown': DB issues or insufficient data.
    
    :param r: Rolling window size in minutes (default: 2 minutes)
    :return: 'idle', 'stable', 'busy', or 'unknown'
    """
    import mysql.connector
    from datetime import datetime

    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)

        # Compute start time for the rolling window using timedelta
        time_threshold = int((datetime.now() - timedelta(minutes=r)).timestamp())

        cursor.execute("""
            SELECT 
                bytesSentRate, bytesReceivedRate,
                packetsRxDropped, packetsTxDropped,
                packetsRxErrors, packetsTxErrors
            FROM port_statistics
            WHERE timestamp >= %s
        """, (time_threshold,))
        
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if not rows:
            print(">> [INFO] No recent data found in port_statistics.")
            return "idle"

        total_sent_rate = 0
        total_recv_rate = 0
        total_drops = 0
        total_errors = 0

        for row in rows:
            total_sent_rate += row["bytesSentRate"] or 0
            total_recv_rate += row["bytesReceivedRate"] or 0
            total_drops += (row["packetsRxDropped"] or 0) + (row["packetsTxDropped"] or 0)
            total_errors += (row["packetsRxErrors"] or 0) + (row["packetsTxErrors"] or 0)

        avg_sent = total_sent_rate / len(rows)
        avg_recv = total_recv_rate / len(rows)

        # Thresholds based on 10Gbps bandwidth
        idle_threshold = 10 * 1e6        # 10 MB/sec
        busy_threshold = 800 * 1e6       # 800 MB/sec
        
        if avg_sent < idle_threshold and avg_recv < idle_threshold and total_drops == 0 and total_errors == 0:
            return "idle"
        elif avg_sent > busy_threshold or avg_recv > busy_threshold or total_drops > 50 or total_errors > 10:
            return "busy"
        else:
            return "stable"
        

    except mysql.connector.Error as err:
        print(f">> [ERROR] DB query failed: {err}")
        return "unknown"


'''
    ACT Module
'''
def push_intent_to_onos(app_id, host_id, new_ip, mac):
    intent = {
        "type": "HostToHostIntent",
        "appId": app_id,
        "priority": 200,
        "one": host_id,
        "two": host_id,
        "constraints": [],
        "selector": {
            "criteria": [
                {"type": "ETH_DST", "mac": mac},
                {"type": "IPV4_DST", "ip": new_ip + "/32"}
            ]
        },
        "treatment": {"instructions": []}
    }
    try:
        response = requests.post(
            f"{ONOS_CONTROLLER}/onos/v1/intents",
            headers={"Content-Type": "application/json"},
            json=intent,
            auth=(USERNAME, PASSWORD)
        )
        if response.status_code in [200, 201]:
            print(f">> [ONOS] Intent successfully pushed for host {host_id} ({new_ip})")
        else:
            print(f">> [ERROR] Intent push failed: {response.status_code}, {response.text}")
    except Exception as e:
        print(f">> [EXCEPTION] Failed to reach ONOS controller: {e}")

'''
STEP 5: 
    Designing the adaptive actions (OpenFlow-based random host mutation for targetted regions) based on the threat severity level
    :Param - Critical == Perform immediate OF-RHM + isolate hosts and block the source IP (where the attacker is)
    :Param - High == Activate OF-RHM + increase flow timeout + notify admin
    :Param - Medium == Log incident + increase monitoring frequency on the flow + Network Health based OF-RHM
    :Param - Low == Log incident + Network-health based OF-RHM + Notify admin
    :Param - None == Continue monitoring 
    :Param - Unkwown == Log incident for forensics or manual review by admin
'''


def response_to_threat(cve_id, severity_label, host_info):
    print(f"\n[DEFENSE] Responding to {cve_id} with severity '{severity_label}'")
    
    if severity_label == "critical":
        print("CRITICAL STATE: Immediately trigger OF-RHM, isolate target host(IP_dst), and block attacker host (IP_src)")
        perform_ofrhm(host_info)   
        isolate_host(host_info)
        block_source_ip(host_info)
        
    elif severity_label == "high":
        print("HIGH: Trigger OF-RHM + increase flow timeout + notify admin")
        perform_ofrhm(host_info)
        increase_flow_timeout()
        notify_admin(cve_id, severity_label)
    
    elif severity_label == "medium":
        log_incident(cve_id, severity_label)
        notify_admin(cve_id, severity_label)
        increase_monitoring_flow()
        network_state = is_network_degraded()
        if network_state == "busy":
            print(">> Network is busy. Avoid OF-RHM.")
            print(f">> [DECISION] OF-RHM skipped for {cve_id} due to BUSY network state.")
        elif network_state == "idle":
            print(">> Network is idle. Safe for mutation.")
            print(f">> [DECISION] OF-RHM performed for {cve_id} in IDLE network state.")
            perform_ofrhm(host_info)
        elif network_state == "stable":
            print(">> Network is stable. Proceed with caution.")
            #Perform selective OF-RHM to be decided
            print(f">> [DECISION] OF-RHM deferred or selectively applied for {cve_id} in STABLE network state.")
        else:
            print(">> Unknown network state. Log this information for the Network Engineer")            
        
    elif severity_label == "none":
        print("None: Continue Monitoring.")
        
    elif severity_label == "Unknown":
        print("Unknown: Log for forensics.")
        log_forensics(cve_id)
        
    else:
        print("Unknown severity level encountered")
        print(f">> [DECISION] OF-RHM not executed for {cve_id} due to UNKNOWN network state.")
        
