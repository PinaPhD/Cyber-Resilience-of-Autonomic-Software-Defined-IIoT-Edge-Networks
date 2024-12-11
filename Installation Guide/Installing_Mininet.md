
## Installing Mininet on the Ubuntu Desktop (GUI) version:

```bash
   sudo apt install git python3-pip -y
```

```bash
   git clone https://github.com/mininet/mininet
```

```bash
   cd mininet
```

```bash
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

