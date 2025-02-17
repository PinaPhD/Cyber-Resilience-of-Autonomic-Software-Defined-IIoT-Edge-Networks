import requests
import json

# ONOS SDN Controller Credentials
ONOS_IP = "10.10.10.43"  # Change to your ONOS controller's IP
USERNAME = "onos"
PASSWORD = "rocks"

# ONOS REST API Endpoint
API_URL = f"http://{ONOS_IP}:8181/onos/v1/network/configuration"

# DHCP Relay Configuration (Define Virtual Interface for DHCP Server)
dhcp_relay_config = {
    "apps": {
        "org.onosproject.dhcprelay": {
            "dhcpServers": [
                {
                    "ip": "192.168.16.254",  # Change to your DHCP server IP
                    "connectPoint": "of:0000000000000001/1"  # Update with your switch ID/port
                }
            ]
        }
    }
}

# Send the DHCP Relay Configuration to ONOS
response = requests.post(
    API_URL,
    auth=(USERNAME, PASSWORD),
    headers={"Content-Type": "application/json"},
    data=json.dumps(dhcp_relay_config)
)

# Print response status
if response.status_code in [200, 204]:
    print("✅ DHCP Relay virtual interface configured successfully!")
else:
    print(f"❌ Error: {response.status_code}, {response.text}")

# Verify the DHCP Relay Configuration
verify_response = requests.get(API_URL, auth=(USERNAME, PASSWORD))

if verify_response.status_code == 200:
    print("\n📌 Current ONOS DHCP Configuration:")
    print(json.dumps(verify_response.json(), indent=4))
else:
    print(f"❌ Error retrieving configuration: {verify_response.status_code}, {verify_response.text}")
