#!/usr/bin/env python3

'''
Ethernet learning switch in Python: HW3.

Note that this file currently has the code to implement a "hub"
in it, not a learning switch.  (I.e., it's currently a switch
that doesn't learn.)
'''
from switchyard.lib.packet import *
from switchyard.lib.address import *
from switchyard.lib.common import *
import time
#switch standard, not able to handle topology changes


def main(net):

    for intf in net.interfaces():
        print (intf.name, intf.ethaddr, intf.ipaddr, intf.netmask)
    #debug use, print out all available ports


    ethaddrTable = dict()
    portList = net.interfaces() 
    ethaddrList = [intf.ethaddr for intf in portList]

    while True:
        try:
            inputPortName,packet = net.recv_packet()
        except Shutdown:
            print ("Got shutdown signal; exiting")
            return
        except NoPackets:
            print ("No packets were available.")
            continue
        except BaseException as e:
            print ("uncatched exception happend when receiving packet: " + str(e))
            return
        # if we get here, we must have received a packet
        
        print ("Received {} on {}".format(packet, inputPortName))
        print("packet headers: "+str(packet.headers()))

        port = net.port_by_name(inputPortName)
        if port is None:
            continue
        #print(type(port))

        ethaddr_src = packet[0].src
        ethaddr_dst = packet[0].dst
        ethaddr_broadcast = EthAddr("ff:ff:ff:ff:ff:ff")

        if ethaddr_src in ethaddrTable and inputPortName!=ethaddrTable[ethaddr_src]:
            oldPortName = ethaddrTable[ethaddr_src]
            ethaddrTable[ethaddr_src] = inputPortName
        elif ethaddr_src not in ethaddrTable:
            ethaddrTable[ethaddr_src] = inputPortName
        #updating forwarding table

        print("ethaddrTable: "+str(ethaddrTable))

        if ethaddr_dst in ethaddrList:
            print("destination is switch itself")
            continue    #destination is switch itself
        elif ethaddr_dst == ethaddr_broadcast or ethaddr_dst not in ethaddrTable :
            print("broadcast")
            for intf in net.interfaces():
                #print (intf.name, intf.ethaddr, intf.ipaddr, intf.netmask)
                if inputPortName != intf.name:
                    net.send_packet(intf.name, packet)
        else:
            print("unicast")
            dstPortName = ethaddrTable[ethaddr_dst]
            dstPort = net.port_by_name(dstPortName)
            net.send_packet(dstPort.name, packet)
        print('*'*100)
        #net.send_packet(inputPortName, packet)














