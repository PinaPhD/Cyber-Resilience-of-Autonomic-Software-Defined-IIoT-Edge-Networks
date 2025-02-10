#!/usr/bin/env python

from mininet.topo import Topo


class sdnnet(Topo):
    "Creating a simple topology to facilitate the IoT-to-ECP Node data"
    def __init__(self):
        "Defining the network topology"
        Topo.__init__(self)

        '''
            OSS rearchitectured as a DataCenter
            Spine-Leaf Switch Network Topology
        '''
        
        # Creating and adding hosts to the topology
        m1 = self.addHost('m1')
        m2 = self.addHost('m2')
        m3 = self.addHost('m3')
        m4 = self.addHost('m4')
        m5 = self.addHost('m5')
        
        q1 = self.addHost('q1')
        q2 = self.addHost('q2')
        q3 = self.addHost('q3')
        q4 = self.addHost('q4')
        q5 = self.addHost('q5')
        
        e1 = self.addHost('e1')
        e2 = self.addHost('e2')
        e3 = self.addHost('e3')
        e4 = self.addHost('e4')
        e5 = self.addHost('e5')
        
        v1 = self.addHost('v1')
        v2 = self.addHost('v2')
        v3 = self.addHost('v3')
        v4 = self.addHost('v4')
        v5 = self.addHost('v5')
        
        # Creating LDAQ and Actuators for the WTGs
        r1 = self.addHost('r1')
        r2 = self.addHost('r2')
        r3 = self.addHost('r3')
        r4 = self.addHost('r4')
        r5 = self.addHost('r5')
        r6 = self.addHost('r6')
        r7 = self.addHost('r7')
        r8 = self.addHost('r8')
        r9 = self.addHost('r9')
        r10 = self.addHost('r10')
        r11 = self.addHost('r11')
        r12 = self.addHost('r12')
        r13 = self.addHost('r13')
        r14 = self.addHost('r14')
        r15 = self.addHost('r15')
        r16 = self.addHost('r16')
        r17 = self.addHost('r17')
        r18 = self.addHost('r18')
        r19 = self.addHost('r19')
        r20 = self.addHost('r20')

        b1 = self.addHost('b1')
        b2 = self.addHost('b2')
        b3 = self.addHost('b3')
        b4 = self.addHost('b4')
        b5 = self.addHost('b5')
        b6 = self.addHost('b6')
        b7 = self.addHost('b7')
        b8 = self.addHost('b8')
        b9 = self.addHost('b9')
        b10 = self.addHost('b10')
        b11 = self.addHost('b11')
        b12 = self.addHost('b12')
        b13 = self.addHost('b13')
        b14 = self.addHost('b14')
        b15 = self.addHost('b15')
        b16 = self.addHost('b16')
        b17 = self.addHost('b17')
        b18 = self.addHost('b18')
        b19 = self.addHost('b19')
        b20 = self.addHost('b20')

        '''
            Creating the ethernet switch network
            Spine-Distribution-Access leaf switch network
        '''
        
        # Spine Switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        
        # Distribution Switches
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')
        s8 = self.addSwitch('s8')
        
        # Access Leaf Switches
        s9 = self.addSwitch('s9')
        s10 = self.addSwitch('s10')
        s11 = self.addSwitch('s11')
        s12 = self.addSwitch('s12')
        s13 = self.addSwitch('s13')
        s14 = self.addSwitch('s14')
        s15 = self.addSwitch('s15')
        s16 = self.addSwitch('s16')
        s17 = self.addSwitch('s17')
        s18 = self.addSwitch('s18')
        s19 = self.addSwitch('s19')
        s20 = self.addSwitch('s20')

        # Create spine-to-spine links (fully connected mesh)
        self.addLink(s1, s2)
        self.addLink(s1, s3)
        self.addLink(s1, s4)
        self.addLink(s2, s3)
        self.addLink(s2, s4)
        self.addLink(s3, s4)

        # Create leaf-to-leaf links (fully connected mesh)
        self.addLink(s5, s6)
        self.addLink(s5, s7)
        self.addLink(s5, s8)
        self.addLink(s6, s7)
        self.addLink(s6, s8)
        self.addLink(s7, s8)

        # Connecting Spine and Distribution Layers
        self.addLink(s1, s5)
        self.addLink(s1, s6)
        self.addLink(s1, s7)
        self.addLink(s1, s8)

        self.addLink(s2, s5)
        self.addLink(s2, s6)
        self.addLink(s2, s7)
        self.addLink(s2, s8)

        self.addLink(s3, s5)
        self.addLink(s3, s6)
        self.addLink(s3, s7)
        self.addLink(s3, s8)

        self.addLink(s4, s5)
        self.addLink(s4, s6)
        self.addLink(s4, s7)
        self.addLink(s4, s8)

        # Connecting the Distribution and Access Layers
        self.addLink(s5, s9)
        self.addLink(s5, s10)
        self.addLink(s5, s11)
        
        self.addLink(s6, s12)
        self.addLink(s6, s13)
        self.addLink(s6, s14)

        self.addLink(s7, s15)
        self.addLink(s7, s16)
        self.addLink(s7, s17)

        self.addLink(s8, s18)
        self.addLink(s8, s19)
        self.addLink(s8, s20)

        # Linking the switches to hosts
        self.addLink(m1, s9)
        self.addLink(m2, s10)
        self.addLink(m3, s11)
        self.addLink(m4, s12)
        self.addLink(m5, s13)
        
        self.addLink(q1, s14)
        self.addLink(q2, s15)
        self.addLink(q3, s16)
        self.addLink(q4, s17)
        self.addLink(q5, s18)
