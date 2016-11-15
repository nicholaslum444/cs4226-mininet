'''
Please add your name: Nicholas Lum Aik Yong
Please add your matric number: A0108358B
'''

import os
import sys
import atexit
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.link import Link
from mininet.link import TCLink
from mininet.node import RemoteController

net = None

class TreeTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)
        f = open('topology.in')
        firstline = f.readline().split(' ')

        numHosts = int(firstline[0])
        numSwitches = int(firstline[1])
        numLinks = int(firstline[2])

        hosts = []
        for i in xrange(numHosts):
            hosts.append(self.addHost('H%d' % (i+1)))

        print hosts

        switches = []
        for i in xrange(numSwitches):
            sconfig = {'dpid': "%016x" % (i+1)}
            switches.append(self.addSwitch('S%d' % (i+1), **sconfig))

        print switches

        links = []
        for i in xrange(numLinks):
            line = f.readline().strip().split(', ')
            print line
            firstNode = line[0]
            secondNode = line[1]
            bandwidth = int(line[2])
            lconfig = {'bw':bandwidth}
            links.append(self.addLink(firstNode, secondNode, **lconfig))


def startNetwork():
    info('** Creating the tree network\n')
    topo = TreeTopo()

    global net
    net = Mininet(topo=topo, link = TCLink,
                  controller=lambda name: RemoteController(name, ip='127.0.0.1'),
                  listenPort=6633, autoSetMacs=True)

    info('** Starting the network\n')
    net.start()

    info('** Creating QoS\n')

    # Create QoS Queues
    os.system('sudo ovs-vsctl -- set Port eth0 qos=@newqos \
                -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000 queues=0=@q0,1=@q1,2=@q2 \
                -- --id=@q0 create queue other-config:max-rate=600000 other-config:min-rate=600000 \
                -- --id=@q1 create queue other-config:min-rate=100000000 \
                -- --id=@q2 create queue other-config:max-rate=50000000')

    info('** Running CLI\n')
    CLI(net)

def stopNetwork():
    if net is not None:
        net.stop()
        # Remove QoS and Queues
        os.system('sudo ovs-vsctl --all destroy Qos')
        os.system('sudo ovs-vsctl --all destroy Queue')


if __name__ == '__main__':
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel('info')
    startNetwork()
