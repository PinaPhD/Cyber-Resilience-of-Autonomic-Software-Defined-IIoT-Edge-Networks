#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class SpineLeafTopo(Topo):
    def build(self):
        # Hosts
        h1 = self.addHost('h1', ip='10.10.10.10/24')
        h2 = self.addHost('h2', ip='10.10.10.15/24')

<<<<<<< HEAD
        # Leaf switches
        leaf1 = self.addSwitch('s1')
        leaf2 = self.addSwitch('s2')

        # Spine switch
        spine = self.addSwitch('s3')

        # Inline switches (between spine and hosts)
        inline1 = self.addSwitch('s4')
        inline2 = self.addSwitch('s5')

        # Connect hosts to leaf switches
        self.addLink(h1, leaf1)
        self.addLink(h2, leaf2)

        # Inline to respective leaf
        self.addLink(inline1, leaf1)
        self.addLink(inline2, leaf2)
        self.addLink(inline1, leaf2)
        self.addLink(inline2, leaf1)
=======
        # Add hosts with real IPs (rIPs)
        h1 = self.addHost('h1', ip='10.10.10.10/24')  # rIP_h1
        h2 = self.addHost('h2', ip='10.10.10.15/24')  # rIP_h2
>>>>>>> 4f40a939df1f76d0bf455b1565eedd181bb28249


def run():
    topo = SpineLeafTopo()
    net = Mininet(topo=topo, controller=RemoteController, switch=OVSSwitch, link=TCLink)

    # ONOS SDN Controller IP
<<<<<<< HEAD
    controller_ip = '10.10.10.43'
=======
    controller_ip = '10.10.10.43'  #  ONOS SDN Controller IP address
>>>>>>> 4f40a939df1f76d0bf455b1565eedd181bb28249
    net.addController('c0', controller=RemoteController, ip=controller_ip, port=6653)

    net.start()

    h1 = net.get('h1')
    h2 = net.get('h2')

    # Assign virtual IPs
<<<<<<< HEAD
    h1.cmd('ip addr add 192.168.1.10/24 dev h1-eth0')
    h1.cmd('ip addr add 172.16.1.15/24 dev h1-eth0')

    h2.cmd('ip addr add 192.168.2.20/24 dev h2-eth0')
    h2.cmd('ip addr add 172.16.2.25/24 dev h2-eth0')
=======
    h1.cmd('ip addr add 192.168.1.10/24 dev h1-eth0')  # vIP1
    h1.cmd('ip addr add 172.16.1.15/24 dev h1-eth0')   # vIP2

    h2.cmd('ip addr add 192.168.2.20/24 dev h2-eth0')  # vIP1
    h2.cmd('ip addr add 172.16.2.25/24 dev h2-eth0')   # vIP2
>>>>>>> 4f40a939df1f76d0bf455b1565eedd181bb28249

    # IPTables setup
    h1.cmd('iptables -F')
    h1.cmd('iptables -P OUTPUT DROP')
<<<<<<< HEAD
    h1.cmd(f'iptables -A OUTPUT -d {controller_ip} -j ACCEPT')
    h1.cmd('iptables -A OUTPUT -s 192.168.1.10 -j ACCEPT')
    h1.cmd('iptables -A OUTPUT -s 172.16.1.15 -j ACCEPT')

    h2.cmd('iptables -F')
    h2.cmd('iptables -P OUTPUT DROP')
    h2.cmd(f'iptables -A OUTPUT -d {controller_ip} -j ACCEPT')
    h2.cmd('iptables -A OUTPUT -s 192.168.2.20 -j ACCEPT')
    h2.cmd('iptables -A OUTPUT -s 172.16.2.25 -j ACCEPT')
=======
    h1.cmd(f'iptables -A OUTPUT -d {controller_ip} -j ACCEPT')  # Allow rIP to ONOS only
    h1.cmd('iptables -A OUTPUT -s 192.168.1.10 -j ACCEPT')  # Allow vIP1 out
    h1.cmd('iptables -A OUTPUT -s 172.16.1.15 -j ACCEPT')   # Allow vIP2 out

    h2.cmd('iptables -F')
    h2.cmd('iptables -P OUTPUT DROP')
    h2.cmd(f'iptables -A OUTPUT -d {controller_ip} -j ACCEPT')  # Allow rIP to ONOS only
    h2.cmd('iptables -A OUTPUT -s 192.168.2.20 -j ACCEPT')  # Allow vIP1 out
    h2.cmd('iptables -A OUTPUT -s 172.16.2.25 -j ACCEPT')   # Allow vIP2 out
>>>>>>> 4f40a939df1f76d0bf455b1565eedd181bb28249

    print("\n>>> h1 interfaces and rules:")
    print(h1.cmd('ip addr show'))
    print(h1.cmd('iptables -L OUTPUT -v'))

    print("\n>>> h2 interfaces and rules:")
    print(h2.cmd('ip addr show'))
    print(h2.cmd('iptables -L OUTPUT -v'))

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
