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
        
        #Creating the SNORT IDS Nodes that are strategically placed in the WTGs, ECP and vPAC server clusters, and for inter-switch between spine and leaf switches
        d1 = self.addHost('d1')
        d2 = self.addHost('d2')
        d3 = self.addHost('d3')
        d4 = self.addHost('d4')
        d5 = self.addHost('d5')
        d6 = self.addHost('d6')
        d7 = self.addHost('d7')
        d8 = self.addHost('d8')
        d9 = self.addHost('d9')
        d10 = self.addHost('d10')
        d11 = self.addHost('d11')
        d12 = self.addHost('d12')
        d13 = self.addHost('d13')
        d14 = self.addHost('d14')
        d15 = self.addHost('d15')
        d16 = self.addHost('d16')
        d17 = self.addHost('d17')
        d18 = self.addHost('d18')
        d19 = self.addHost('d19')
        d20 = self.addHost('d20')
        d21 = self.addHost('d21')
        d22 = self.addHost('d22')
        d23 = self.addHost('d23')
        d24 = self.addHost('d24')
        d25 = self.addHost('d25')
        d26 = self.addHost('d26')
        
        
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
        f1 = self.addSwitch('f1')
        
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

        # Create spine-to-spine switch links (Building redundancy)
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s4)
        self.addLink(s2, f1)

        # Connecting Spine and Distribution Layers (Building redundancy)
        self.addLink(s1, s5)
        self.addLink(s1, s6)
        self.addLink(s1, s7)
        self.addLink(s1, s8)
        self.addLink(s1, d26)

        self.addLink(s2, s5)
        self.addLink(s2, s6)
        self.addLink(s2, s7)
        self.addLink(s2, s8)
        self.addLink(s2, d25)

        self.addLink(s3, s5)
        self.addLink(s3, s6)
        self.addLink(s3, s7)
        self.addLink(s3, s8)
        self.addLink(s3, d24)

        self.addLink(s4, s5)
        self.addLink(s4, s6)
        self.addLink(s4, s7)
        self.addLink(s4, s8)
        self.addLink(s4, d23)

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

        self.addLink(e1,s19)
        self.addLink(e2,s20)
        self.addLink(e3,s10)
        self.addLink(d21,s10)
        self.addLink(e4,s19)
        self.addLink(e5,s13)
        
        self.addLink(v1,s12)
        self.addLink(v2,s11)
        self.addLink(v3,s15)
        self.addLink(d22,s15)
        self.addLink(v4,s17)
        self.addLink(v5,s19)

        ''' 
           Wind Farm WTG access networks
        '''
       
        #Creating switches for 20 wind turbine generator Nacelle and Tower access networks (Reduced-scale model) 
        s21 = self.addSwitch('s21')
        s22 = self.addSwitch('s22')
        s23 = self.addSwitch('s23')
        s24 = self.addSwitch('s24')
        s25 = self.addSwitch('s25')
        s26 = self.addSwitch('s26')
        s27 = self.addSwitch('s27')
        s28 = self.addSwitch('s28')
        s29 = self.addSwitch('s29')
        s30 = self.addSwitch('s30')
        s31 = self.addSwitch('s31')
        s32 = self.addSwitch('s32')
        s33 = self.addSwitch('s33')
        s34 = self.addSwitch('s34')
        s35 = self.addSwitch('s35')
        s36 = self.addSwitch('s36')
        s37 = self.addSwitch('s37')
        s38 = self.addSwitch('s38')
        s39 = self.addSwitch('s39')
        s40 = self.addSwitch('s40')

        #Linking these switches to the spine switches
        self.addLink(s21,s1)
        self.addLink(s22,s1)
        self.addLink(s23,s1)
        self.addLink(s24,s1)
        self.addLink(s25,s1)

        self.addLink(s26,s2)
        self.addLink(s27,s2)
        self.addLink(s28,s2)
        self.addLink(s29,s2)
        self.addLink(s30,s2)

        self.addLink(s31,s3)
        self.addLink(s32,s3)
        self.addLink(s33,s3)
        self.addLink(s34,s3)
        self.addLink(s35,s3)

        self.addLink(s36,s4)
        self.addLink(s37,s4)
        self.addLink(s38,s4)
        self.addLink(s39,s4)
        self.addLink(s40,s4)

        #Linking local data acquisition modules and actuators to each wtg switches
        self.addLink(r1, s21)
        self.addLink(b1, s21)
        self.addLink(d1, s21)

        self.addLink(r2, s22)
        self.addLink(b2, s22)
        self.addLink(d2, s22)

        self.addLink(r3, s23)
        self.addLink(b3, s23)
        self.addLink(d3, s23)

        self.addLink(r4, s24)
        self.addLink(b4, s24)
        self.addLink(d4, s24)

        self.addLink(r5, s25)
        self.addLink(b5, s25)
        self.addLink(d5, s25)

        self.addLink(r6, s26)
        self.addLink(b6, s26)
        self.addLink(d6, s26)

        self.addLink(r7, s27)
        self.addLink(b7, s27)
        self.addLink(d7, s27)

        self.addLink(r8, s28)
        self.addLink(b8, s28)
        self.addLink(d8, s28)

        self.addLink(r9, s29)
        self.addLink(b9, s29)
        self.addLink(d9, s29)

        self.addLink(r10, s30)
        self.addLink(b10, s30)
        self.addLink(d10, s30)

        self.addLink(r11, s31)
        self.addLink(b11, s31)
        self.addLink(d11, s31)

        self.addLink(r12, s32)
        self.addLink(b12, s32)
        self.addLink(d12, s32)

        self.addLink(r13, s33)
        self.addLink(b13, s33)
        self.addLink(d13, s33)

        self.addLink(r14, s34)
        self.addLink(b14, s34)
        self.addLink(d14, s34)

        self.addLink(r15, s35)
        self.addLink(b15, s35)
        self.addLink(d15, s35)

        self.addLink(r16, s36)
        self.addLink(b16, s36)
        self.addLink(d16, s36)

        self.addLink(r17, s37)
        self.addLink(b17, s37)
        self.addLink(d17, s37)

        self.addLink(r18, s38)
        self.addLink(b18, s38)
        self.addLink(d18, s38)

        self.addLink(r19, s39)
        self.addLink(b19, s39)
        self.addLink(d19, s39)

        self.addLink(r20, s40)
        self.addLink(b20, s40)
        self.addLink(d20, s40)

    
topos = {'mytopo': (lambda: sdnnet() )}

