#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Sun Feb 16 20:27:17 2025
    @Task: 
        - Reading the SNORT logs from the data plane and storing the information to a knowledge base (InfluxDB/MySQL)
        - Reading the Network Health State from the data plane and storing this information to a knowledge base (InfluxDB/MySQL)
    @author: agrippina Mwangi 
"""

import requests
import time
import logging
import pandas as pd
import mysql.connector
from datetime import datetime
import json  # Import JSON module to convert dict to string


'''
    ONOS SDN controller cluster interacting with the Knowledge Base
    Connecting to the primary SDN controller using a 8181 RESTful API based url and 
    BASE24 Authentication (Plain user/password credentials)
'''

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Prompting user for ONOS controller details
print("OBSERVE MODULE AS(n) OT Network Topology.\n Disclaimer: Press Enter if you wish to use the default configurations\n\n")
controller_ip = input("Enter the IP address of the ONOS controller (default is 10.10.10.43: )")
controller_ip = controller_ip if controller_ip else '10.10.10.43'
onos_base_url = f'http://{controller_ip}:8181/onos/v1'

username = input("Enter the username for ONOS controller (default is 'onos'): ")
username = username if username else 'onos'
password = input("Enter the password for ONOS controller (default is 'rocks'): ")
password = password if password else 'rocks'
onos_auth = (username, password)

#Connecting to the knowledge base
DB_HOST = "10.10.10.30"
DB_USER = "pina254"
DB_PASSWORD = "Baarn@2026_"
DB_NAME = "KNOWLEDGE_BASE"

def get_devices():
    """ 
        Fetches network devices from the ONOS controller. 
    """
    
    try:
        response = requests.get(f'{onos_base_url}/devices', auth=onos_auth)
        if response.status_code == 200:
            devices = response.json().get('devices', [])
            df = pd.DataFrame(devices)
            return df
        else:
            print(f"Failed to retrieve Network devices: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching Network devices: {e}")

def get_links():
    """ 
        Fetches network links from the ONOS controller. 
    """
    
    try:
        response = requests.get(f'{onos_base_url}/links', auth=onos_auth)
        if response.status_code == 200:
            links = response.json().get('links', [])
            df = pd.DataFrame(links)
            return df
        else:
            print(f"Failed to retrieve Network links: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching Network Links: {e}")

def get_hosts():
    """ 
        Fetches network hosts from the ONOS controller. 
    """

    try:
        response = requests.get(f'{onos_base_url}/hosts', auth=onos_auth)
        if response.status_code == 200:
            hosts = response.json().get('hosts', [])
            df = pd.DataFrame(hosts)
            return df
        else:
            print(f"Failed to retrieve Network hosts: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching Network hosts: {e}")

def get_flows():
    """ 
        Fetches flow rules from the ONOS controller. 
    """
    
    try:
        response = requests.get(f'{onos_base_url}/flows', auth=onos_auth)
        if response.status_code == 200:
            flows = response.json().get('flows', [])
            df = pd.DataFrame(flows)
            return df
        else:
            print(f"Failed to retrieve Network flows: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching Network flows: {e}")

def get_port_statistics():
    """ 
        Fetches port statistics from all devices in the ONOS controller. 
    """
    
    try:
        response = requests.get(f'{onos_base_url}/statistics/ports', auth=onos_auth)
        if response.status_code == 200:
            port_stats = response.json().get('statistics', [])
            # Flatten the nested JSON structure for easier CSV writing
            flattened_stats = []
            for device in port_stats:
                device_id = device['device']
                for port in device['ports']:
                    port['device'] = device_id
                    flattened_stats.append(port)
            df = pd.DataFrame(flattened_stats)
            return df
        else:
            print(f"Failed to retrieve Port Statistics: Status code {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching network port statistics: {e}")


    
'''
STEP 1: Read SNORT Logs from the different IDSs mounted on the switch network in the data plane and insert them to the Knowledge_Base through Barnyard2
 --- OBSERVE Module  
'''
            
def get_snort_logs():
    """
    Fetches SNORT alerts from the Barnyard2-populated MySQL database and returns them as a DataFrame.
    Assumes standard schema from SNORT/Barnyard2 (schema.sql).
    """

    conn = None
    cursor = None

    try:
        # Connect to the MySQL database where Barnyard2 stores alerts
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)

        # SQL query to fetch recent SNORT alerts (customize as needed)
        query = """
        SELECT
            event.cid,
            event.signature,
            signature.sig_name,
            inet_ntoa(ip_hdr.ip_src) AS src_ip,
            inet_ntoa(ip_hdr.ip_dst) AS dst_ip,
            ip_hdr.ip_proto,
            tcphdr.tcp_sport,
            tcphdr.tcp_dport,
            event.timestamp
        FROM
            event
        JOIN
            signature ON event.signature = signature.sig_id
        JOIN
            ip_hdr ON event.cid = ip_hdr.cid AND event.sid = ip_hdr.sid
        LEFT JOIN
            tcphdr ON event.cid = tcphdr.cid AND event.sid = tcphdr.sid
        ORDER BY
            event.timestamp DESC
        LIMIT 100;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        df = pd.DataFrame(results)
        logging.info(f"Retrieved {len(df)} SNORT alerts from Barnyard2 database.")
        return df

    except mysql.connector.Error as err:
        logging.error(f"Error querying SNORT logs from Barnyard2: {err}")
        return pd.DataFrame()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    
def current_network_state():
    devices = get_devices()
    links = get_links()
    hosts = get_hosts()
    flows = get_flows()
    port_stats = get_port_statistics()
    snort_logs = get_snort_logs()
       
    return devices, links, hosts, flows, port_stats, snort_logs

'''
Inserting records into the database
'''
def insert_flows_into_db(flows_df):
    """ Inserts flow records into MySQL database, replacing duplicates with the latest entry """

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

        # SQL DELETE statement (remove old record if it exists)
        delete_sql = "DELETE FROM flow_records WHERE id = %s"

        # SQL INSERT statement
        insert_sql = """
        INSERT INTO flow_records (
            id, groupId, state, life, liveType, lastSeen, packets, bytes, 
            appId, priority, timeout, isPermanent, deviceId, tableId, tableName, treatment, selector
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Loop through DataFrame and insert/update rows
        for _, row in flows_df.iterrows():
            cursor.execute(delete_sql, (row['id'],))  # Delete the existing record
            cursor.execute(insert_sql, (
                row.get('id', None),
                row.get('groupId', None),
                row.get('state', None),
                row.get('life', None),
                row.get('liveType', None),
                row.get('lastSeen', None),
                row.get('packets', None),
                row.get('bytes', None),
                row.get('appId', None),
                row.get('priority', None),
                row.get('timeout', None),
                row.get('isPermanent', None),
                row.get('deviceId', None),
                row.get('tableId', None),
                row.get('tableName', None),
                json.dumps(row.get('treatment', {})),  # Convert dictionary to JSON string
                json.dumps(row.get('selector', {}))  # Convert dictionary to JSON string
            ))

        # Commit transaction
        conn.commit()
        print(f"Inserted {cursor.rowcount} records into flow_records.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_devices_into_db(devices_df):
    """ Inserts device records into MySQL database, replacing duplicates with the latest entry """

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

        # SQL DELETE statement (remove old record if it exists)
        delete_sql = "DELETE FROM device_records WHERE id = %s"

        # SQL INSERT statement
        insert_sql = """
        INSERT INTO device_records (
            id, type, available, role, mfr, hw, sw, serial, driver, chassisId,
            lastUpdate, humanReadableLastUpdate, annotations
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Loop through DataFrame and insert/update rows
        for _, row in devices_df.iterrows():
            cursor.execute(delete_sql, (row['id'],))  # Delete the existing record
            cursor.execute(insert_sql, (
                row.get('id', None),
                row.get('type', None),
                row.get('available', None),
                row.get('role', None),
                row.get('mfr', None),
                row.get('hw', None),
                row.get('sw', None),
                row.get('serial', None),
                row.get('driver', None),
                row.get('chassisId', None),
                row.get('lastUpdate', None),
                row.get('humanReadableLastUpdate', None),
                json.dumps(row.get('annotations', {}))  # Convert dictionary to JSON string
            ))

        # Commit transaction
        conn.commit()
        print(f"Inserted {cursor.rowcount} records into device_records.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_links_into_db(links_df):
    """ Inserts or updates link records into MySQL database """

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

        # SQL DELETE statement (remove old record if it exists)
        delete_sql = """
        DELETE FROM link_records WHERE src_device = %s AND src_port = %s AND dst_device = %s AND dst_port = %s
        """

        # SQL INSERT statement
        insert_sql = """
        INSERT INTO link_records (
            src_device, src_port, dst_device, dst_port, type, state
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Loop through DataFrame and insert/update rows
        for _, row in links_df.iterrows():
            src_device = row['src']['device']
            src_port = row['src']['port']
            dst_device = row['dst']['device']
            dst_port = row['dst']['port']

            cursor.execute(delete_sql, (src_device, src_port, dst_device, dst_port))  # Delete the existing record
            cursor.execute(insert_sql, (
                src_device, src_port, dst_device, dst_port, row.get('type', None), row.get('state', None)
            ))

        # Commit transaction
        conn.commit()
        print(f"Inserted {cursor.rowcount} records into link_records.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_port_statistics_into_db(port_stats_df):
    """ Inserts port statistics into MySQL while computing rates. """

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

        # SQL Insert Statement
        sql = """
        INSERT INTO port_statistics (
            timestamp, port, device, packetsReceived, packetsSent, bytesReceived, bytesSent,
            packetsRxDropped, packetsTxDropped, packetsRxErrors, packetsTxErrors, durationSec,
            bytesReceivedRate, bytesSentRate, packetsReceivedRate, packetsSentRate
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Retrieve last known stats for each port-device pair
        cursor.execute("""
            SELECT port, device, durationSec, packetsReceived, packetsSent, bytesReceived, bytesSent 
            FROM port_statistics ORDER BY timestamp DESC LIMIT 1
        """)
        prev_data = cursor.fetchall()
        prev_stats = {(row[0], row[1]): row[2:] for row in prev_data}  # Map (port, device) → previous stats

        # Loop through DataFrame and insert rows
        for _, row in port_stats_df.iterrows():
            port = row.get('port', 0)
            device = row.get('device', '')
            durationSec = row.get('durationSec', 0)
            packetsReceived = row.get('packetsReceived', 0)
            packetsSent = row.get('packetsSent', 0)
            bytesReceived = row.get('bytesReceived', 0)
            bytesSent = row.get('bytesSent', 0)
            packetsRxDropped = row.get('packetsRxDropped', 0)
            packetsTxDropped = row.get('packetsTxDropped', 0)
            packetsRxErrors = row.get('packetsRxErrors', 0)
            packetsTxErrors = row.get('packetsTxErrors', 0)
            timestamp = int(time.time())  # UNIX timestamp

            # Fetch previous entry if exists
            prev_entry = prev_stats.get((port, device))

            if prev_entry:
                prev_durationSec, prev_packetsReceived, prev_packetsSent, prev_bytesReceived, prev_bytesSent = prev_entry

                # Ensure no division by zero
                time_diff = max(1, durationSec - prev_durationSec)

                # Compute rates (ensuring they are float values)
                bytes_received_rate = float((bytesReceived - prev_bytesReceived) / time_diff)
                bytes_sent_rate = float((bytesSent - prev_bytesSent) / time_diff)
                packets_received_rate = float((packetsReceived - prev_packetsReceived) / time_diff)
                packets_sent_rate = float((packetsSent - prev_packetsSent) / time_diff)

            else:
                # First-time entry, set rates to 0.0
                bytes_received_rate = 0.0
                bytes_sent_rate = 0.0
                packets_received_rate = 0.0
                packets_sent_rate = 0.0

            # Insert into database
            cursor.execute(sql, (
                timestamp,
                port,
                device,
                packetsReceived,
                packetsSent,
                bytesReceived,
                bytesSent,
                packetsRxDropped,
                packetsTxDropped,
                packetsRxErrors,
                packetsTxErrors,
                durationSec,
                bytes_received_rate,
                bytes_sent_rate,
                packets_received_rate,
                packets_sent_rate
            ))

        # Commit transaction
        conn.commit()
        print(f"Inserted {cursor.rowcount} records into port_statistics.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_threat_to_db(Z, level):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Baarn@2026_',
        database='KNOWLEDGE_BASE'
    )
    cursor = conn.cursor()
    timestamp = datetime.now()
    sql = "INSERT INTO threat_levels (timestamp, z_value, threat_level) VALUES (%s, %s, %s)"
    cursor.execute(sql, (timestamp, Z, level))
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    try:
        while True:
            print("\nPress **Ctrl + C** to stop execution... Running data collection & insertion...\n")
            
            
            
            '''
            STEP 2: Assess the network health and categorize it as either busy, stable, or idle.
            '''
            # Reading the current network state
            devices, links, hosts, flows, port_stats, snort_logs = current_network_state()

            # Insert flows into DB
            if flows is not None and not flows.empty:
                insert_flows_into_db(flows)
            else:
                print("No flow records available for insertion.")
            
            # Insert devices into DB
            if devices is not None and not devices.empty:
                insert_devices_into_db(devices)
            else:
                print("No device records available for insertion.")

            # Insert links into DB
            if links is not None and not links.empty:
                insert_links_into_db(links)
            else:
                print("No link records available for insertion.")

            # Insert port statistics into DB
            if port_stats is not None and not port_stats.empty:
                insert_port_statistics_into_db(port_stats)
            else:
                print("No port statistics available for insertion.")
            
            
            
            
            # Sleep for 1 second before the next iteration
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nUser requested to stop. Exiting the MTD Framework...")
