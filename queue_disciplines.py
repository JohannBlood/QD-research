def switch_config_cbq(net, k=2):
    for i in range(1, k + 1):
        switch = net.get(f's{i}')
        switch.cmd(f'tc qdisc del dev s{i}-eth1 root')
        print(switch.cmd(f'tc qdisc add dev s{i}-eth1 root handle 1:0 cbq avpkt 1000 bandwidth 100Mbit cell 8'))
        print(switch.cmd(f'tc class add dev s{i}-eth1 parent 1:0 classid 1:1 cbq bandwidth 100Mbit rate 10Mbit weight 1Mbit prio 8 allot 1514 cell 8 maxburst 20 avpkt 1000'))
        print(switch.cmd(f'tc class add dev s{i}-eth1 parent 1:1 classid 1:3 cbq bandwidth 100Mbit rate 60Mbit weight 6Mbit prio 5 allot 1514 cell 8 maxburst 20 avpkt 1000 bounded'))
        print(switch.cmd(f'tc class add dev s{i}-eth1 parent 1:1 classid 1:4 cbq bandwidth 100Mbit rate 30Mbit weight 3Mbit prio 5 allot 1514 cell 8 maxburst 20 avpkt 1000 bounded'))
        print(switch.cmd(f'tc class add dev s{i}-eth1 parent 1:1 classid 1:5 cbq bandwidth 100Mbit rate 10Mbit weight 1Mbit prio 5 allot 1514 cell 8 maxburst 20 avpkt 1000 bounded'))
        print(switch.cmd(f'tc filter add dev s{i}-eth1 protocol ip parent 1:0 prio 1 u32 match ip tos 0x10 0xff flowid 1:3'))
        print(switch.cmd(f'tc filter add dev s{i}-eth1 protocol ip parent 1:0 prio 1 u32 match ip tos 0x08 0xff flowid 1:4'))
        print(switch.cmd(f'tc filter add dev s{i}-eth1 protocol ip parent 1:0 prio 1 u32 match ip tos 0x04 0xff flowid 1:5'))
        # switch.cmd(f'tc filter show dev s{i}-eth1 > log{i}.txt')
        # switch.cmd(f'tc qdisc show dev s{i}-eth1 > log{i}.txt')
        # switch.cmd(f'tcpdump -i s{i}-eth1 > tcpdump{i}.txt')


def host_config_cbq(net, k=2):
    for i in range(1, k + 1):
        host = net.get(f'h{i}')
        host.cmd(f'tc qdisc del dev h{i}-eth0 root')
        host.cmd(f'tc qdisc add dev h{i}-eth0 root handle 1:0 cbq avpkt 1000 bandwidth 100Mbit cell 8')
        host.cmd(f'tc class add dev h{i}-eth0 parent 1:0 classid 1:1 cbq bandwidth 100Mbit rate 10Mbit weight 1Mbit prio 8 allot 1514 cell 8 maxburst 20 avpkt 1000')
        host.cmd(f'tc class add dev h{i}-eth0 parent 1:1 classid 1:3 cbq bandwidth 100Mbit rate 60Mbit weight 6Mbit prio 5 allot 1514 cell 8 maxburst 20 avpkt 1000 bounded')
        host.cmd(f'tc class add dev h{i}-eth0 parent 1:1 classid 1:4 cbq bandwidth 100Mbit rate 30Mbit weight 3Mbit prio 5 allot 1514 cell 8 maxburst 20 avpkt 1000 bounded')
        host.cmd(f'tc class add dev h{i}-eth0 parent 1:1 classid 1:5 cbq bandwidth 100Mbit rate 10Mbit weight 1Mbit prio 5 allot 1514 cell 8 maxburst 20 avpkt 1000 bounded')
        host.cmd(f'tc filter add dev h{i}-eth0 protocol ip parent 1:0 prio 1 u32 match ip tos 0x10 0xff flowid 1:3')
        host.cmd(f'tc filter add dev h{i}-eth0 protocol ip parent 1:0 prio 1 u32 match ip tos 0x08 0xff flowid 1:4')
        host.cmd(f'tc filter add dev h{i}-eth0 protocol ip parent 1:0 prio 1 u32 match ip tos 0x04 0xff flowid 1:5')
        # host.cmd(f'tc filter show dev h{i}-eth0 > log{i}.txt')
        # host.cmd(f'tc filter show dev h{i}-eth0 > log{i}.txt')
        # switch.cmd(f'tcpdump -i s{i}-eth1 > tcpdump{i}.txt')


def switch_config_fq(net, k=2):
    for i in range(1, k + 1):
        switch = net.get(f's{i}')
        switch.cmd(f'tc qdisc del dev s{i}-eth1 root')
        print(switch.cmd(f'tc qdisc add dev s{i}-eth1 root fq'))
        print(switch.cmd(f'tc qdisc show dev s{i}-eth1'))


def host_config_fq(net, k=2):
    for i in range(1, k + 1):
        host = net.get(f'h{i}')
        host.cmd(f'tc qdisc del dev h{i}-eth0 root')
        print(host.cmd(f'tc qdisc add dev h{i}-eth0 root fq'))
