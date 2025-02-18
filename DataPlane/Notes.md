

---
Very important Linux commands when working with SNORT IDS in the Mininet Controlled Environment
---

##### Reconnaissance Attacks and late-stage DDoS and Cross-Fire Attacks

- To insert new SNORT IDS local rules: `sudo nano /etc/snort/rules/local.rules`

- To set a SNORT IDS node in Mininet to detect an attack: `sudo snort -A console -q -c /etc/snort/snort.conf -i d5-eth0`

- To run an NMAP reconnaissance attack: `nmap -sS <here replace with ip address/ip address range>`