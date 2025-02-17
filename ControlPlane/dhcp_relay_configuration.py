import requests
import json
import datetime

# ONOS SDN Controller Credentials
ONOS_IP = "10.10.10.43"  # Change to your ONOS controller's IP
USERNAME = "onos"
PASSWORD = "rocks"

# ONOS REST API Endpoint
API_URL = f"http://{ONOS_IP}:8181/onos/v1/network/configuration"

# Generate a timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# DHCP Relay Configuration (Define Virtual Interface for DHCP Server)
dhcp_relay_config = {
    "apps": {
        "org.onosproject.dhcprelay": {
            "dhcpServers": [
                {
                    "ip": "192.168.16.254",  # DHCP Server IP based on the DHCP subnet pools
                    "connectPoint": "of:0000000000000001/15"  # Switch Port to connect to DHCP server
                }
            ],
            "dhcpManager": {
                "allowHostDiscovery": True  # Allow host discovery from DHCP requests
            },
            "dhcpFpmEnabled": True  # Enable DHCP Forwarding Policy Manager
        },
        "org.onosproject.hostlocationprovider": {
            "useDhcp": True  # Enable DHCP to automatically assign IP addresses to hosts
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

    # Verify the DHCP Relay Configuration
    verify_response = requests.get(API_URL, auth=(USERNAME, PASSWORD))

    if verify_response.status_code == 200:
        dhcp_config = verify_response.json()
        print("\n📌 Current ONOS DHCP Configuration:")
        print(json.dumps(dhcp_config, indent=4))

        # Save configuration to a file with a timestamp
        file_path = f"dhcp_relay_config_{timestamp}.txt"
        with open(file_path, "w") as file:
            json.dump(dhcp_config, file, indent=4)

        print(f"✅ DHCP Relay configuration saved to {file_path}")

    else:
        print(f"❌ Error retrieving configuration: {verify_response.status_code}, {verify_response.text}")

else:
    print(f"❌ Error: {response.status_code}, {response.text}")
