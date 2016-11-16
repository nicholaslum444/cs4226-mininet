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
            switch = self.addSwitch('S%d' % (i+1), **sconfig)
            switches.append(switch)

        print switches
        print self.switches()

        self.linkConfigs = []
        for i in xrange(numLinks):
            line = f.readline().strip().split(', ')
            print line
            self.linkConfigs.append(line)
            firstNode = line[0]
            secondNode = line[1]
            # add link without bandwidth since the bandwidth will be added later in queue
            self.addLink(firstNode, secondNode)

        print self.links(True, False, True)


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
    def getLinkSpeedBps(firstNode, secondNode):
        for config in topo.linkConfigs:
            if firstNode == config[0] and secondNode == config[1]:
                # originally in Mbps, mult by 1mil to change to bps
                return int(config[2]) * 1000000

        return 0

    nints = 0
    # get switch interfaces
    for link in topo.links(True, False, True):
        for switch in topo.switches():
            linkInfo = link[2]
            for i in [1, 2]:
                if linkInfo["node%i" % (i)] == switch:
                    nints += 1
                    port = linkInfo["port%i" % (i)]
                    firstNode = linkInfo["node1"]
                    secondNode = linkInfo["node2"]
                    linkSpeed = getLinkSpeedBps(firstNode, secondNode)
                    xSpeed = 100000000 # 100mbps
                    ySpeed = 50000000 # 50mbps
                    interface = "%s-eth%s" % (switch, port)
                    # OS system call
                    os.system("sudo ovs-vsctl -- set Port %s qos=@newqos \
                        -- --id=@newqos create QoS type=linux-htb other-config:max-rate=%i queues=0=@q0,1=@q1,2=@q2 \
                        -- --id=@q0 create queue other-config:max-rate=%i other-config:min-rate=%i \
                        -- --id=@q1 create queue other-config:min-rate=%i \
                        -- --id=@q2 create queue other-config:max-rate=%i" % (interface, linkSpeed, linkSpeed, linkSpeed, xSpeed, ySpeed))

    print "QoS set up on %i interfaces" % (nints)

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
