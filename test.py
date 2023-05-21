#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from multiprocessing import Process
from queue_disciplines import *
import json

SZ = 2

class LinearTopo(Topo):
    "Linear topology of k switches, with one host per switch."

    def __init__(self, k=2, **opts):
        """Init.
            k: number of switches (and hosts)
            hconf: host configuration options
            lconf: link configuration options"""

        super(LinearTopo, self).__init__(**opts)

        self.k = k

        lastSwitch = None
        for i in irange(1, k):
            host = self.addHost('h%s' % i, cpu=.5/k)
            switch = self.addSwitch('s%s' % i)
            # 100 Mbps, 5ms delay, 1% loss, 1000 packet queue
            self.addLink( host, switch, bw=100, delay='5ms', loss=0, max_queue_size=1000, use_htb=True)
            if lastSwitch:
                self.addLink(switch, lastSwitch, bw=100, delay='5ms', loss=0, max_queue_size=1000, use_htb=True)
            lastSwitch = switch


def udp_iperf3(h1, h2):
    h1.cmd('iperf3 -s -i 1 -J -p 5001 > logs/udp_server_1.txt &')
    h1.cmd('iperf3 -s -i 1 -J -p 5002 > logs/udp_server_2.txt &')
    h1.cmd('iperf3 -s -i 1 -J -p 5003 > logs/udp_server_3.txt &')
    h2.cmd(f'iperf3 -c {h1.IP()} -p 5001 -u -b 10Mbit -t 10 -S 0x10 -i 1 > logs/udp_1.txt & iperf3 -c {h1.IP()} -p 5002 -u -b 10Mbit -t 10 -S 0x08 -i 1 > logs/udp_2.txt & iperf3 -c {h1.IP()} -p 5003 -u -b 10Mbit -t 10 -S 0x04 -i 1 > logs/udp_3.txt')
    

def udp_iperf2(h1, h2):
    h1.cmd('iperf -s -u -i 1 -p 5001 > logs/udp_server.txt &')
    h2.cmd(f'iperf -c {h1.IP()} -p 5001 -u -b 100Mbit -t 10 -S 0x10 -i 1 > logs/udp_1.txt & iperf -c {h1.IP()} -p 5001 -u -P 2 -b 100Mbit -t 10 -S 0x08 -i 1 > logs/udp_2.txt & iperf -c {h1.IP()} -p 5001 -u -b 100Mbit -t 10 -S 0x04 -i 1 > logs/udp_3.txt')


def tcp_iperf3(h1, h2, parallel):
    h1.cmd('iperf3 -s -i 1 -p 5001 > logs/tcp_server_1.txt &')
    h1.cmd('iperf3 -s -i 1 -p 5002 > logs/tcp_server_2.txt &')
    h1.cmd('iperf3 -s -i 1 -p 5003 > logs/tcp_server_3.txt &')
    h2.cmd(f'iperf3 -c {h1.IP()} -p 5001 -t 5 -l 1000 -i 1 -P {parallel} -J t -S 0x10 > logs/tcp_1.txt & iperf3 -c {h1.IP()} -p 5002 -t 5 -l 1000 -i 1 -P {parallel} -J  -S 0x08 > logs/tcp_2.txt & iperf3 -c {h1.IP()} -p 5003 -t 5 -l 1000 -i 1 -P {parallel} -J  -S 0x04 > logs/tcp_3.txt')



def perfTest():
    "Create network and run simple performance test"
    topo = LinearTopo(k=2)
    net = Mininet(topo=topo, link=TCLink)
    net.start()

    switch_config_cbq(net, 2)
    host_config_cbq(net, 2)

    # switch_config_fq(net, 2)
    # host_config_fq(net, 2)

    # s4.cmd('tc filter show dev s4-eth1 > log.txt')

    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    print("Testing bandwidth between h1 and h2")

    # CLI(net)

    h1, h2 = net.get('h1', 'h2')

    out = open('res.txt', 'w')
    out2 = open('res2.txt', 'w')

    for j in range(1, 5):
        tcp_iperf3(h1, h2, 1)

        h2.cmd('sleep 10')

        for i in range(1, 4):
            f = open(f'logs/tcp_{i}.txt', 'r')
            cl = json.load(f)
            out.write(str(max(cl['end']['streams'], key=lambda x: x['sender']['max_rtt'])['sender']['max_rtt']) + '\n')
            out2.write(str(round(cl['end']['sum_sent']["bits_per_second"] / 1024 / 1024, 2)) + '\n')

        h1.cmd('pkill iperf3')

    # s1, s1 = net.get('s1', 's2')
    # print("Switch statistics")
    # print(s1.cmd('tc -s filter show dev s1-eth1 parent 1:'))

    # print("Host statistics")
    # print(h2.cmd('tc -s qdisc show dev h2-eth0'))
    # print(h2.cmd('tc -s filter show dev h2-eth0 parent 1:'))

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    perfTest()