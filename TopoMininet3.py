#!/usr/bin/python

# Code found on stackoverflow using this search
#
# https://stackoverflow.com/questions/46595423/mininet-how-to-create-a-topology-with-two-routers-and-their-respective-hosts

#
# Fall 2023: Computer Networks
#
# Used in explaining the programmatic approach to build topologies
#
# Run this program under "sudo" mode
#
# I have added comments to explain the code.  Note that this code is
# probably written with Python2 syntax.
#
# Here is a text base diagram of what they are trying to accomplish

# host(d1) -- switch (s1) -- router (r1) --- router (r2) -- switch (s2) -- host (d2)
# d1 will have IP address: 10.0.0.251
# d2 will have IP address: 10.1.0.252  (note it is in a diff n/w than d1)
# Note that switches are bridges
# r1 will have IP address: 10.0.0.1 facing its LAN and 10.100.0.1 facing r2
# r2 will have IP address: 10.1.0.1 facing its LAN and 10.100.0.2 facing r1
#
# Our aim is for d1 and d2 to talk to each other.

# Many of the packages that need to be imported. See
# https://mininet.org/api/index.html
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


# The author has used this class from the mininet/examples directory. It shows
# how to create a router. IP forwarding is enabled when the router is activated
# and then disabled at the time of termination.
class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


# Here, they are building the entire network topology. This is a class definition
# that inherits from the base Topo class
class NetworkTopo(Topo):
    # Our code must provide this overridden method
    def build(self, **_opts):
        # Add 2 routers in two different subnets. The addHost method on the
        # Topo class adds a Node type. Here we specifically tell it what node
        # type it is by passing the cls=LinuxRouter and passing what IP
        # address we would like on that interface
        Q = self.addHost('Q', cls=LinuxRouter, ip='192.168.10.1/24')
        P = self.addHost('P', cls=LinuxRouter, ip='172.16.3.1/24')
        R = self.addHost('R', cls=LinuxRouter, ip='172.12.0.1/16')
        S = self.addHost('S', cls=LinuxRouter, ip='192.167.10.1/24')
        T = self.addHost('T', cls=LinuxRouter, ip='192.167.9.1/24')
        V = self.addHost('V', cls=LinuxRouter, ip='10.100.0.1/16')
        U = self.addHost('U', cls=LinuxRouter, ip='10.85.8.1/24')

        # Add switches
        sq = self.addSwitch('sq', dpid='0000000000000001')
        sp1 = self.addSwitch('sp1', dpid='0000000000000002')
        sp2 = self.addSwitch('sp2', dpid='0000000000000003')
        sr = self.addSwitch('sr', dpid='0000000000000004')
        sv = self.addSwitch('sv', dpid='0000000000000005')
        su1 = self.addSwitch('su1', dpid='0000000000000006')
        su2 = self.addSwitch('su2', dpid='0000000000000007')
        ss = self.addSwitch('ss', dpid='0000000000000008')
        st = self.addSwitch('st', dpid='0000000000000009')

        # Add host-switch links in the same subnet.  We need this because now
        # we want to connect our routers to their respective switches. We must also
        # name the interfaces, here r1-eth1 and so on, and make sure to assign an
        # IP address facing the LAN.
        self.addLink(sq,
                     Q,
                     intfName2='q-eth1',
                     params2={'ip': '192.168.10.1/24'})

        self.addLink(sp1,
                     P,
                     intfName2='p-eth1',
                     params2={'ip': '172.16.3.1/24'})

        self.addLink(sp2,
                     P,
                     intfName2='p-eth2',
                     params2={'ip': '172.16.5.1/24'})
        self.addLink(sr,
                     R,
                     intfName2='r-eth1',
                     params2={'ip': '172.12.0.1/16'})
        self.addLink(su1,
                     U,
                     intfName2='u-eth1',
                     params2={'ip': '10.85.10.1/24'})
        self.addLink(su2,
                     U,
                     intfName2='u-eth2',
                     params2={'ip': '10.85.8.1/24'})
        self.addLink(sv,
                     V,
                     intfName2='v-eth1',
                     params2={'ip': '10.100.0.1/16'})
        self.addLink(ss,
                     S,
                     intfName2='s-eth111',
                     params2={'ip': '192.167.10.1/24'})
        self.addLink(st,
                     T,
                     intfName2='t-eth111',
                     params2={'ip': '192.167.9.1/24'})


        # Add link between routers
        self.addLink(P,
                     Q,
                     intfName1='p-eth3',
                     intfName2='q-eth2',
                     params1={'ip': '10.101.1.1/24'},
                     params2={'ip': '10.101.1.2/24'})
        self.addLink(Q,
                     S,
                     intfName1='q-eth3',
                     intfName2='s-eth1',
                     params1={'ip': '10.101.2.1/24'},
                     params2={'ip': '10.101.2.2/24'})
        self.addLink(Q,
                     V,
                     intfName1='q-eth4',
                     intfName2='v-eth2',
                     params1={'ip': '10.101.3.1/24'},
                     params2={'ip': '10.101.3.2/24'})
        self.addLink(T,
                     Q,
                     intfName1='t-eth1',
                     intfName2='q-eth5',
                     params1={'ip': '10.101.4.1/24'},
                     params2={'ip': '10.101.4.2/24'})
        self.addLink(V,
                     T,
                     intfName1='v-eth3',
                     intfName2='t-eth2',
                     params1={'ip': '10.101.5.1/24'},
                     params2={'ip': '10.101.5.2/24'})
        self.addLink(S,
                     V,
                     intfName1='s-eth2',
                     intfName2='v-eth4',
                     params1={'ip': '10.101.6.1/24'},
                     params2={'ip': '10.101.6.2/24'})
        self.addLink(S,
                     R,
                     intfName1='s-eth3',
                     intfName2='r-eth2',
                     params1={'ip': '10.101.7.1/24'},
                     params2={'ip': '10.101.7.2/24'})
        self.addLink(V,
                     U,
                     intfName1='v-eth5',
                     intfName2='u-eth3',
                     params1={'ip': '10.101.8.1/24'},
                     params2={'ip': '10.101.8.2/24'})
        self.addLink(U,
                     S,
                     intfName1='u-eth4',
                     intfName2='s-eth4',
                     params1={'ip': '10.101.9.1/24'},
                     params2={'ip': '10.101.9.2/24'})
        self.addLink(R,
                     U,
                     intfName1='r-eth3',
                     intfName2='u-eth5',
                     params1={'ip': '10.101.10.1/24'},
                     params2={'ip': '10.101.10.2/24'})
        self.addLink(R,
                     P,
                     intfName1='r-eth4',
                     intfName2='p-eth4',
                     params1={'ip': '10.101.11.1/24'},
                     params2={'ip': '10.101.11.2/24'})



        # Adding hosts specifying the default route
        dq = self.addHost(name='dq',
                          ip='192.168.10.2/24',
                          defaultRoute='via 192.168.10.1')
        dp1 = self.addHost(name='dp1',
                          ip='172.16.3.2/24',
                          defaultRoute='via 172.16.3.1')
        dp2 = self.addHost(name='dp2',
                          ip='172.16.5.2/24',
                          defaultRoute='via 172.16.5.1')
        dr = self.addHost(name='dr',
                          ip='172.12.0.2/16',
                          defaultRoute='via 172.12.0.1')
        du1 = self.addHost(name='du1',
                          ip='10.85.10.2/24',
                          defaultRoute='via 10.85.10.1')
        du2 = self.addHost(name='du2',
                          ip='10.85.8.2/24',
                          defaultRoute='via 10.85.8.1')
        dv = self.addHost(name='dv',
                          ip='10.100.0.2/16',
                          defaultRoute='via 10.100.0.1')
        ds = self.addHost(name='ds',
                          ip='192.167.10.2/24',
                          defaultRoute='via 192.167.10.1')
        dt = self.addHost(name='dt',
                          ip='192.167.9.2/24',
                          defaultRoute='via 192.167.9.1')




        # Add host-switch links
        self.addLink(dq, sq)
        self.addLink(dp1, sp1)
        self.addLink(dp2, sp2)
        self.addLink(dr, sr)
        self.addLink(du1, su1)
        self.addLink(du2, su2)
        self.addLink(dv, sv)
        self.addLink(ds, ss)
        self.addLink(dt, st)


def run():
    # first, instantiate our topology. Recall that everything is hardcoded in this
    # topology
    topo = NetworkTopo()

    # Then create the network object from this topology
    net = Mininet(topo=topo)

    # Note how the "ip route add" command is invoked on each router so that
    # they can route to each other

    net.addNAT(name='nat1', ip='10.0.44.1').configDefault()
    net.addLink(net['P'], net['nat1'],
                intfName1='p-nat-eth', params1={'ip':'10.0.43.2/24'},
                intfName2='nat-p-eth', params2={'ip':'10.0.43.1/24'})
    # Add routing for reaching networks that aren't directly connected
    info(net['nat1'].cmd('ip route add 192.168.10.0/24 via 10.0.43.2 dev nat-p-eth'))
    info(net['nat1'].cmd('ip route add 172.16.5.0/24 via 10.0.43.2 dev nat-p-eth'))
    info(net['nat1'].cmd('ip route add 172.16.3.0/24 via 10.0.43.2 dev nat-p-eth'))
    info(net['nat1'].cmd('ip route add 172.12.0.0/16 via 10.0.43.2 dev nat-p-eth'))
    info(net['nat1'].cmd('ip route add 10.85.8.0/24 via 10.0.43.2 dev nat-p-eth'))
    info(net['nat1'].cmd('ip route add 10.85.10.0/24 via 10.0.43.2 dev nat-p-eth'))
    info(net['nat1'].cmd('ip route add 10.100.0.0/16 via 10.0.43.2 dev nat-p-eth'))
    info(net['nat1'].cmd('ip route add 192.167.10.0/24 via 10.0.43.2 dev nat-p-eth'))
    info(net['nat1'].cmd('ip route add 192.167.9.0/24 via 10.0.43.2 dev nat-p-eth'))

    info(net['nat1'].cmd('ip route add default via 192.168.100.1 dev vxlan0'))
    info(net['nat1'].cmd('iptables -D FORWARD -i nat1-eth0 -d 10.0.0.0/8 -j DROP'))

    # P to Q
    info(net['P'].cmd("ip route add 192.168.10.0/24 via 10.101.1.2 dev p-eth3"))
    # to S
    info(net['P'].cmd("ip route add 192.167.10.0/24 via 10.101.1.2 dev p-eth3"))
    # to T
    info(net['P'].cmd("ip route add 192.167.9.0/24 via 10.101.1.2 dev p-eth3"))
    # to V
    info(net['P'].cmd("ip route add 10.100.0.0/16 via 10.101.1.2 dev p-eth3"))
    # to U
    info(net['P'].cmd("ip route add 10.85.8.0/24 via 10.101.1.2 dev p-eth3"))
    info(net['P'].cmd("ip route add 10.85.10.0/24 via 10.101.1.2 dev p-eth3"))
    # to R
    info(net['P'].cmd("ip route add 172.12.0.0/16 via 10.101.1.2 dev p-eth3"))
    # default
    info(net['P'].cmd("ip route add default via 10.101.1.2 dev p-eth3"))
    # to NAT
    info(net['P'].cmd("ip route add 10.0.44.0/24 via 10.0.43.1 dev p-nat-eth"))



    # Q to V
    info(net['Q'].cmd("ip route add 10.100.0.0/16 via 10.101.2.2 dev q-eth3"))
    # to U
    info(net['Q'].cmd("ip route add 10.85.8.0/24 via 10.101.2.2 dev q-eth3"))
    info(net['Q'].cmd("ip route add 10.85.10.0/24 via 10.101.2.2 dev q-eth3"))
    # to R
    info(net['Q'].cmd("ip route add 172.12.0.0/16 via 10.101.2.2 dev q-eth3"))
    # to P
    info(net['Q'].cmd("ip route add 172.16.3.0/24 via 10.101.2.2 dev q-eth3"))
    info(net['Q'].cmd("ip route add 172.16.5.0/24 via 10.101.2.2 dev q-eth3"))
    # to S
    info(net['Q'].cmd("ip route add 192.167.10.0/24 via 10.101.2.2 dev q-eth3"))
    # to T
    info(net['Q'].cmd("ip route add 192.167.9.0/24 via 10.101.2.2 dev q-eth3"))
    # default
    info(net['Q'].cmd("ip route add default via 10.101.2.2 dev q-eth3"))
    # to NAT
    info(net['Q'].cmd("ip route add 10.0.44.0/24 via 10.101.2.2 dev q-eth3"))




    # V to T
    info(net['V'].cmd("ip route add 192.167.9.0/24 via 10.101.5.2 dev v-eth3"))
    # to Q
    info(net['V'].cmd("ip route add 192.168.10.0/24 via 10.101.5.2 dev v-eth3"))
    # to S
    info(net['V'].cmd("ip route add 192.167.10.0/24 via 10.101.5.2 dev v-eth3"))
    # to U
    info(net['V'].cmd("ip route add 10.85.8.0/24 via 10.101.8.2 dev v-eth5"))
    info(net['V'].cmd("ip route add 10.85.10.0/24 via 10.101.8.2 dev v-eth5"))
    # to P
    info(net['V'].cmd("ip route add 172.16.3.0/24 via 10.101.5.2 dev v-eth3"))
    info(net['V'].cmd("ip route add 172.16.5.0/24 via 10.101.5.2 dev v-eth3"))
    # to R
    info(net['V'].cmd("ip route add 172.12.0.0/16 via 10.101.5.2 dev v-eth3"))
    # default
    info(net['V'].cmd("ip route add default via 10.101.5.2 dev v-eth3"))
    # P to NAT
    info(net['V'].cmd("ip route add 10.0.44.0/24 via 10.101.5.2 dev v-eth3"))



    # T to Q
    info(net['T'].cmd("ip route add 192.168.10.0/24 via 10.101.4.2 dev t-eth1"))
    # to V
    info(net['T'].cmd("ip route add 10.100.0.0/16 via 10.101.4.2 dev t-eth1"))
    # to S
    info(net['T'].cmd("ip route add 192.167.10.0/24 via 10.101.4.2 dev t-eth1"))
    # to U
    info(net['T'].cmd("ip route add 10.85.8.0/24 via 10.101.4.2 dev t-eth1"))
    info(net['T'].cmd("ip route add 10.85.10.0/24 via 10.101.4.2 dev t-eth1"))
    # to P
    info(net['T'].cmd("ip route add 172.16.3.0/24 via 10.101.4.2 dev t-eth1"))
    info(net['T'].cmd("ip route add 172.16.5.0/24 via 10.101.4.2 dev t-eth1"))
    # to R
    info(net['T'].cmd("ip route add 172.12.0.0/16 via 10.101.4.2 dev t-eth1"))
    # default
    info(net['T'].cmd("ip route add default via 10.101.4.2 dev t-eth1"))
    # P to NAT
    info(net['T'].cmd("ip route add 10.0.44.0/24 via 10.101.4.2 dev t-eth1"))




    # S to V
    info(net['S'].cmd("ip route add 10.100.0.0/16 via 10.101.6.2 dev s-eth2"))
    # to Q
    info(net['S'].cmd("ip route add 192.168.10.0/24 via 10.101.6.2 dev s-eth2"))
    # to T
    info(net['S'].cmd("ip route add 192.167.9.0/24 via 10.101.6.2 dev s-eth2"))
    # to U
    info(net['S'].cmd("ip route add 10.85.8.0/24 via 10.101.6.2 dev s-eth2"))
    info(net['S'].cmd("ip route add 10.85.10.0/24 via 10.101.6.2 dev s-eth2"))
    # to R
    info(net['S'].cmd("ip route add 172.12.0.0/16 via 10.101.7.2 dev s-eth3"))
    # to P
    info(net['S'].cmd("ip route add 172.16.3.0/24 via 10.101.7.2 dev s-eth3"))
    info(net['S'].cmd("ip route add 172.16.5.0/24 via 10.101.7.2 dev s-eth3"))
    # default
    info(net['S'].cmd("ip route add default via 10.101.6.2 dev s-eth2"))
    # P to NAT
    info(net['S'].cmd("ip route add 10.0.44.0/24 via 10.101.6.2 dev s-eth2"))




    # U to S
    info(net['U'].cmd("ip route add 192.167.10.0/24 via 10.101.9.2 dev u-eth4"))
    # to V
    info(net['U'].cmd("ip route add 10.100.0.0/16 via 10.101.9.2 dev u-eth4"))
    # to T
    info(net['U'].cmd("ip route add 192.167.9.0/24 via 10.101.9.2 dev u-eth4"))
    # to Q
    info(net['U'].cmd("ip route add 192.168.10.0/24 via 10.101.9.2 dev u-eth4"))
    # to P
    info(net['U'].cmd("ip route add 172.16.3.0/24 via 10.101.9.2 dev u-eth4"))
    info(net['U'].cmd("ip route add 172.16.5.0/24 via 10.101.9.2 dev u-eth4"))
    # to R
    info(net['U'].cmd("ip route add 172.12.0.0/16 via 10.101.9.2 dev u-eth4"))
    # default
    info(net['U'].cmd("ip route add default via 10.101.9.2 dev u-eth4"))
    # P to NAT
    info(net['U'].cmd("ip route add 10.0.44.0/24 via 10.101.9.2 dev u-eth4"))






    # R to P
    info(net['R'].cmd("ip route add 172.16.3.0/24 via 10.101.11.2 dev r-eth4"))
    info(net['R'].cmd("ip route add 172.16.5.0/24 via 10.101.11.2 dev r-eth4"))
    # to Q
    info(net['R'].cmd("ip route add 192.168.10.0/24 via 10.101.11.2 dev r-eth4"))
    # to T
    info(net['R'].cmd("ip route add 192.167.9.0/24 via 10.101.11.2 dev r-eth4"))
    # to V
    info(net['R'].cmd("ip route add 10.100.0.0/16 via 10.101.11.2 dev r-eth4"))
    # to S
    info(net['R'].cmd("ip route add 192.167.10.0/24 via 10.101.11.2 dev r-eth4"))
    # to U
    info(net['R'].cmd("ip route add 10.85.8.0/24 via 10.101.10.2 dev r-eth3"))
    info(net['R'].cmd("ip route add 10.85.10.0/24 via 10.101.10.2 dev r-eth3"))
    # default
    info(net['R'].cmd("ip route add default via 10.101.11.2 dev r-eth4"))
    # P to NAT
    info(net['R'].cmd("ip route add 10.0.44.0/24 via 10.101.11.2 dev r-eth4"))



    info(net['dq'].cmd('ip route add default via 192.168.10.1'))
    info(net['dp1'].cmd('ip route add default via 172.16.3.1'))
    info(net['dp2'].cmd('ip route add default via 172.16.5.1'))
    info(net['dr'].cmd('ip route add default via 172.12.0.1'))
    info(net['du1'].cmd('ip route add default via 10.85.10.1'))
    info(net['du2'].cmd('ip route add default via 10.85.8.1'))
    info(net['dv'].cmd('ip route add default via 10.100.0.1'))
    info(net['ds'].cmd('ip route add default via 192.167.10.1'))
    info(net['dt'].cmd('ip route add default via 192.167.9.1'))




    net.start()  # this method must be invoked to start the mininet
    CLI(net)  # this gives us mininet prompt
    net.stop()  # this cleans up the network


if __name__ == '__main__':
    setLogLevel('info')
    run()