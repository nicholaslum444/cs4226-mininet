'''
Please add your name: Nicholas Lum Aik Yong
Please add your matric number: A0108358B
'''

import sys
import os
from sets import Set

from pox.core import core

import pox.openflow.libopenflow_01 as of
import pox.openflow.discovery
import pox.openflow.spanning_tree

from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.addresses import IPAddr, EthAddr

log = core.getLogger()

class Controller(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        core.openflow_discovery.addListeners(self)
        self.mac_port_table = {}

    def _handle_PacketIn (self, event):
        print dir(event)
        print event
        packet = event.parsed
        if not packet.parsed:
            log.warning("ignoring incomplete packet")
            return

        print "packet---"
        print packet
        print "packet src---"
        print packet.src
        print "packet src port---"
        print event.port
        print "packet dest---"
        print packet.dst
        src_port = event.port
        self.mac_port_table[str(packet.src)] = src_port

        # actual ofp_packet_in message
        packet_in = event.ofp
        print "ofp packet---"
        print packet_in

        # always flood
        self.flood2(event, packet_in)
        return

        # get the dst port, if not exist, flood
        if str(packet.dst) not in self.mac_port_table:
            print "flood packet---"
            self.flood(event, packet_in)
            return

        # else send msg to port
        dst_port = self.mac_port_table[str(packet.dst)]
        print "packet dest port---"
        print dst_port

        # send msg directly to port and add rule
        msg = of.ofp_flow_mod()
        msg.match.dl_src = packet.src
        msg.match.dl_dst = packet.dst
        msg.actions.append(of.ofp_action_output(port = dst_port))
        print "msg out---"
        print msg
        event.connection.send(msg)

    # When it knows nothing about the destination, flood but don't install the rule
    def flood (self, event, packet_in):
        msg = of.ofp_packet_out()
        msg.data = packet_in
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        print "packet out---"
        print msg
        event.connection.send(msg)

    def flood2(self, event, packet_in):
        msg = of.ofp_flow_mod()
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        event.connection.send(msg)
        print "packet out2---"
        print msg

    def _handle_ConnectionUp(self, event):
        dpid = dpid_to_str(event.dpid)
        log.debug("Switch %s has come up.", dpid)

    # Send the firewall policies to the switch
    #def sendFirewallPolicy(connection, policy):
        #for i in firewall policies:
        #sendFirewallPolicy(event.connection, i)

def launch():
    # Run discovery and spanning tree modules
    pox.openflow.discovery.launch()
    pox.openflow.spanning_tree.launch()

    # Starting the controller module
    core.registerNew(Controller)
