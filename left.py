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
# d1 will have IP address: 10.1.0.100
# d2 will have IP address: 10.2.0.100  (note it is in a diff n/w than d1)
# Note that switches are bridges
# r1 will have IP address: 10.1.0.1 facing its LAN and 10.50.0.1 facing r2
# r2 will have IP address: 10.2.0.1 facing its LAN and 10.50.0.2 facing r1
#
# Our aim is for d1 and d2 to talk to each other.

# Many of the packages that need to be imported. See
# https://mininet.org/api/index.html
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.nodelib import NAT
from mininet.log import setLogLevel, info
from mininet.cli import CLI

# The author has used this class from the mininet/examples directory. It shows
# how to create a router. IP forwarding is enabled when the router is activated
# and then disabled at the time of termination.
class LinuxRouter (Node):
    def config (self, **params):
        super (LinuxRouter, self).config (**params)
        self.cmd ('sysctl net.ipv4.ip_forward=1')
    def terminate (self):
        self.cmd ('sysctl net.ipv4.ip_forward=0')
        super (LinuxRouter, self).terminate ()


# Here, they are building the entire network topology. This is a class definition
# that inherits from the base Topo class
class NetworkTopo (Topo):
    # Our code must provide this overridden method
    def build(self, **_opts):
        # Add 2 routers in two different subnets. The addHost method on the
        # Topo class adds a Node type. Here we specifically tell it what node
        # type it is by passing the cls=LinuxRouter and passing what IP
        # address we would like on that interface
        r1 = self.addHost ('r1', cls=LinuxRouter, ip='10.1.0.1/24')
        r2 = self.addHost ('r2', cls=LinuxRouter, ip='10.2.0.1/24')
        r3 = self.addHost ('r3', cls=LinuxRouter, ip='10.3.0.1/24')
        # Add 2 switches
        s1 = self.addSwitch ('s1')
        s2 = self.addSwitch ('s2')
        #s3 = self.addSwitch ('s3')
        
        nat = self.addNode('nat', cls=NAT, ip='10.3.0.100/24', inNamespace=False)
        # Add host-switch links in the same subnet.  We need this because now
        # we want to connect our routers to their respective switches. We must also
        # name the interfaces, here r1-eth1 and so on, and make sure to assign an
        # IP address facing the LAN.
        self.addLink (s1,
                     r1,
                     intfName2='r1-eth1',
                     params2={'ip': '10.1.0.1/24'})
        self.addLink (s2,
                     r2,
                     intfName2='r2-eth1',
                     params2={'ip': '10.2.0.1/24'})
        """
        self.addLink (s3,
                     r3,
                     intfName2='r3-eth1',
                     params2={'ip': '10.3.0.1/24'})
        """
        self.addLink(nat, r3, intfName2='nat-eth0', params2={'ip': '10.3.0.100/24'})

        # Add router-router link in a new subnet for the router-router connection
        self.addLink(r1,
                     r2,
                     intfName1='r1-eth12',
                     intfName2='r2-eth12',
                     params1={'ip': '10.50.0.1/24'},
                     params2={'ip': '10.50.0.2/24'})
        #"""
        self.addLink(r1,
                     r3,
                     intfName1='r1-eth13',
                     intfName2='r3-eth13',
                     params1={'ip': '10.50.0.1/24'},
                     params2={'ip': '10.50.0.3/24'})
                     
        self.addLink(r2,
                     r3,
                     intfName1='r2-eth23',
                     intfName2='r3-eth23',
                     params1={'ip': '10.50.0.2/24'},
                     params2={'ip': '10.50.0.3/24'})
        #"""        
        # Adding hosts specifying the default route
        d1 = self.addHost (name='d1',
                          ip='10.1.0.100/24',
                          defaultRoute='via 10.1.0.1')
        d2 = self.addHost (name='d2',
                          ip='10.2.0.100/24',
                          defaultRoute='via 10.2.0.1')
        """
        d3 = self.addHost (name='d3',
                          ip='10.3.0.100/24',
                          defaultRoute='via 10.3.0.1')
        """
        # Add host-switch links
        self.addLink (d1, s1)
        self.addLink (d2, s2)
        """
        self.addLink (d3, s3)
        """


def run():
     # first, instantiate our topology. Recall that everything is hardcoded in this
    # topology
    topo = NetworkTopo ()

    # Then create the network object from this topology
    net = Mininet (topo=topo)

    # Note how the "ip route add" command is invoked on each router so that
    # they can route to each other
    
    # Add routing for reaching networks that aren't directly connected
    info (net['r1'].cmd("ip route add 10.2.0.0/24 via 10.50.0.2 dev r1-eth12"))
    info (net['r2'].cmd("ip route add 10.1.0.0/24 via 10.50.0.1 dev r2-eth12"))
    info (net['r1'].cmd("ip route add 10.3.0.0/24 via 10.50.0.3 dev r1-eth13"))
    info (net['r3'].cmd("ip route add 10.1.0.0/24 via 10.50.0.1 dev r3-eth13"))
    info (net['r2'].cmd("ip route add 10.3.0.0/24 via 10.50.0.3 dev r2-eth23"))
    info (net['r3'].cmd("ip route add 10.2.0.0/24 via 10.50.0.2 dev r3-eth23"))
        
    info (net['r1'].cmd("ip route add 10.100.0.0/16 via 10.50.0.3 dev r1-eth13"))
    info (net['r2'].cmd("ip route add 10.100.0.0/16 via 10.50.0.3 dev r2-eth23"))
    info (net['r3'].cmd("ip route add 10.100.0.0/16 via 10.3.0.1 dev r3-eth1"))

    net.start ()  # this method must be invoked to start the mininet
    CLI (net)   # this gives us mininet prompt
    net.stop ()  # this cleans up the network


if __name__ == '__main__':
    setLogLevel('info')
    run()
