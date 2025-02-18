

---
Very important Linux commands when working with SNORT IDS in the Mininet Controlled Environment
---

##### Reconnaissance Attacks and late-stage DDoS and Cross-Fire Attacks

- To insert new SNORT IDS local rules: `sudo nano /etc/snort/rules/local.rules`

- To set a SNORT IDS node in Mininet to detect an attack: `sudo snort -A console -q -c /etc/snort/snort.conf -i d5-eth0`

- To run an NMAP reconnaissance attack: `nmap -sS <here replace with ip address/ip address range>`

- To enable IP Forwarding for better traffic flow: `sudo sysctl -w net.ipv4.ip_forward=1`

- To launch a SYN Flood (DDoS) attack from multiple hosts targeting a victim (ECP node) or (vPAC node): `e4 hping3 -S --flood -p 80 b5`  and `v3 hping3 -S --flood -p 80 r20`

- To launch a UDP Flood attack:  `v4 hping3 --udp -p 80 --flood e1`  - E1 is the MQTT broker in this network topology.

- To launch cross-fire attacks (where attackers flood multiple strategic nodes in a network to disrupt a critical communication path by identifying the bottleneck links and those that carry critical traffic then generating malicious background traffic on these links from multiple mininet hosts): 
	```bash
	h1 iperf -c h4 -u -b 100M -t 60 &
	h2 iperf -c h4 -u -b 100M -t 60 &
	h3 iperf -c h5 -u -b 100M -t 60 &
	```