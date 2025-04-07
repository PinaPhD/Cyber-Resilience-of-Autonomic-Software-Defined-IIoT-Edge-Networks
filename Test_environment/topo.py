#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class MultiIPTopo(Topo):
    def build(self):
        # Add switch
        s1 = self.addSwitch('s1')

        # Add hosts with real IPs (rIPs)
        h1 = self.addHost('h1', ip='10.10.10.10/24')  # rIP_h1
        h2 = self.addHost('h2', ip='10.10.10.15/24')  # rIP_h2

        self.addLink(h1, s1)
        self.addLink(h2, s1)

def run():
    topo = MultiIPTopo()
    net = Mininet(topo=topo, controller=RemoteController, switch=OVSSwitch, link=TCLink)

    # ONOS SDN Controller IP
    controller_ip = '10.10.10.43'  #  ONOS SDN Controller IP address
    net.addController('c0', controller=RemoteController, ip=controller_ip, port=6653)

    net.start()

    h1 = net.get('h1')
    h2 = net.get('h2')

    # Assign virtual IPs
    h1.cmd('ip addr add 192.168.1.10/24 dev h1-eth0')  # vIP1
    h1.cmd('ip addr add 172.16.1.15/24 dev h1-eth0')   # vIP2

    h2.cmd('ip addr add 192.168.2.20/24 dev h2-eth0')  # vIP1
    h2.cmd('ip addr add 172.16.2.25/24 dev h2-eth0')   # vIP2

    # Flush any existing rules and default policies
    h1.cmd('iptables -F')
    h1.cmd('iptables -P OUTPUT DROP')
    h1.cmd(f'iptables -A OUTPUT -d {controller_ip} -j ACCEPT')  # Allow rIP to ONOS only
    h1.cmd('iptables -A OUTPUT -s 192.168.1.10 -j ACCEPT')  # Allow vIP1 out
    h1.cmd('iptables -A OUTPUT -s 172.16.1.15 -j ACCEPT')   # Allow vIP2 out

    h2.cmd('iptables -F')
    h2.cmd('iptables -P OUTPUT DROP')
    h2.cmd(f'iptables -A OUTPUT -d {controller_ip} -j ACCEPT')  # Allow rIP to ONOS only
    h2.cmd('iptables -A OUTPUT -s 192.168.2.20 -j ACCEPT')  # Allow vIP1 out
    h2.cmd('iptables -A OUTPUT -s 172.16.2.25 -j ACCEPT')   # Allow vIP2 out

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
