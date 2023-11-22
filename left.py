#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter (Node):
    def config (self, **params):
        super (LinuxRouter, self).config (**params)
        self.cmd ('sysctl net.ipv4.ip_forward=1')

    def terminate (self):
        self.cmd ('sysctl net.ipv4.ip_forward=0')
        super (LinuxRouter, self).terminate ()


class NetworkTopo (Topo):

    def build(self, **_opts):
        router1 = self.addNode('r1', cls=LinuxRouter, ip='10.1.0.1/24')
        router2 = self.addNode('r2', cls=LinuxRouter, ip='10.2.0.1/24')
        router3 = self.addNode('r3', cls=LinuxRouter, ip='10.3.0.1/24')
        #        
        
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        switch3 = self.addSwitch('s3')
        #
        

        host1 = self.addHost('h1', ip='10.1.0.253/24', defaultRoute='via 10.1.0.1')
        host2 = self.addHost('h2', ip='10.2.0.100/24', defaultRoute='via 10.2.0.1')
        host3 = self.addHost('h3', ip='10.3.0.100/24', defaultRoute='via 10.3.0.1')
        #
        

        
        #
        self.addLink(host1, switch1)
        self.addLink(host2, switch2)
        self.addLink(host3, switch3)

        #
        self.addLink(switch1, router1, intfName2='r1-s1-eth', params2={'ip':'10.1.0.1/24'})
        self.addLink(switch2, router2, intfName2='r2-s2-eth', params2={'ip':'10.2.0.1/24'})
        self.addLink(switch3, router3, intfName2='r3-s3-eth', params2={'ip':'10.3.0.1/24'})
        
        
        #"""
        self.addLink('r1', 'r2', intfName1='r1-r2-eth', intfName2='r2-r1-eth',
                     params1={'ip': '10.12.0.1/24'}, params2={'ip': '10.12.0.2/24'})
        self.addLink('r1', 'r3', intfName1='r1-r3-eth', intfName2='r3-r1-eth',
                     params1={'ip': '10.13.0.1/24'}, params2={'ip': '10.13.0.3/24'})
        #"""
        self.addLink('r3', 'r2', intfName1='r3-r2-eth', intfName2='r2-r3-eth',
                     params1={'ip': '10.23.0.3/24'}, params2={'ip': '10.23.0.2/24'})
        
def run():
    # Then create the network object from this topology
    net = Mininet(topo=NetworkTopo())

    net.addNAT(name='nat1', ip='10.0.42.1').configDefault()
    net.addLink(net['r3'], net['nat1'],
                intfName1='r3-nat-eth', params1={'ip':'10.0.41.1/24'},
                intfName2='nat-r3-eth', params2={'ip':'10.0.41.2/24'})
    
    info(net['nat1'].cmd('ip route add 10.1.0.0/24 via 10.0.41.1 dev nat-r3-eth'))
    info(net['nat1'].cmd('ip route add 10.2.0.0/24 via 10.0.41.1 dev nat-r3-eth'))
    info(net['nat1'].cmd('ip route add 10.3.0.0/24 via 10.0.41.1 dev nat-r3-eth'))
    info(net['nat1'].cmd('ip route add default via 192.168.100.2 dev vxlan0'))
    info(net['nat1'].cmd('iptables -D FORWARD -i nat1-eth0 -d 10.0.0.0/8 -j DROP'))
    #"""
    info(net['r1'].cmd('ip route add 10.2.0.0/24 via 10.12.0.2 dev r1-r2-eth'))
    info(net['r1'].cmd('ip route add 10.3.0.0/24 via 10.13.0.3 dev r1-r3-eth'))
    info(net['r1'].cmd('ip route add 10.0.42.0/24 via 10.13.0.3 dev r1-r3-eth'))
    info(net['r1'].cmd('ip route add default via 10.12.0.2 dev r1-r2-eth'))
    #"""
    #
    info(net['r2'].cmd('ip route add 10.1.0.0/24 via 10.12.0.1 dev r2-r1-eth'))
    info(net['r2'].cmd('ip route add 10.3.0.0/24 via 10.23.0.3 dev r2-r3-eth'))
    info(net['r2'].cmd('ip route add 10.0.42.0/24 via 10.23.0.3 dev r2-r3-eth'))
    info(net['r2'].cmd('ip route add default via 10.23.0.3 dev r2-r3-eth'))
    #
    info(net['r3'].cmd('ip route add 10.1.0.0/24 via 10.13.0.1 dev r3-r1-eth'))
    info(net['r3'].cmd('ip route add 10.2.0.0/24 via 10.23.0.2 dev r3-r2-eth'))
    info(net['r3'].cmd('ip route add 10.0.42.0/24 via 10.0.41.2 dev r3-nat-eth'))
    info(net['r3'].cmd('ip route add default via 10.0.41.2 dev r3-nat-eth'))

    #
    info(net['h1'].cmd('ip route add default via 10.1.0.1'))
    info(net['h2'].cmd('ip route add default via 10.2.0.1'))    
    info(net['h3'].cmd('ip route add default via 10.3.0.1'))
    
    
    
    
    info( '*** Starting network\n')
    net.start ()  # this method must be invoked to start the mininet

    
    info( '*** Running CLI\n' )
    CLI (net)   # this gives us mininet prompt

    info( '*** Stopping network' )
    net.stop ()  # this cleans up the network


if __name__ == '__main__':
    setLogLevel('info')
    run()
