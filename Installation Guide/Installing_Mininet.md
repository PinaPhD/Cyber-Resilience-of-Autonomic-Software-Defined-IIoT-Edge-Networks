
## Installing Mininet on the Ubuntu Desktop (GUI) version:

```bash
   sudo apt install git python3-pip -y
   git clone https://github.com/mininet/mininet
   cd mininet
   sudo ./util/install.sh -a
```

Running the offshore WPP Network Topology [AS1 Network Topology](https://github.com/PinaPhD/JP3/blob/main/DataPlane/dataplane.py)

In the Mininet CLI prompt, using xterm instantiate the data transfers between all the communicating nodes (IIoT sensors, Merging Units, vIEDs, ECP units, and actuators)

```bash
   xterm <host_name> <host_name> <host_name> ...
```

Running Wireshark:

```bash
   sudo -E wireshark
```

## Installing MQTT Mosquitto for the IoT to ECP pub/sub model
```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
mosquitto -v
```

Open the MQTT Mosquitto configuration file and update:
```bash
listener 1883 0.0.0.0
allow_anonymous true
```

Restart the MQTT mosquitto broker
```bash
pkill mosquitto
mosquitto -c mqtt.conf -v
```