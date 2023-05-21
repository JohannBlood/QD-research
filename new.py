s1 tc qdisc add dev s1-eth1 root handle 1:0 cbq avpkt 1000 bandwidth 10Mbit
s1 tc class add dev s1-eth1 parent 1:0 classid 1:1 cbq rate 3Mbit weight 1 allot 1514
s1 tc class add dev s1-eth1 parent 1:0 classid 1:2 cbq rate 5Mbit weight 2 allot 1514
s1 tc class add dev s1-eth1 parent 1:0 classid 1:3 cbq rate 2Mbit weight 3 allot 1514
s1 tc filter add dev s1-eth1 protocol ip parent 1:0 prio 1 u32 match ip tos 0x10 0xff flowid 1:1
s1 tc filter add dev s1-eth1 protocol ip parent 1:0 prio 2 u32 match ip tos 0x08 0xff flowid 1:2
s1 tc filter add dev s1-eth1 protocol ip parent 1:0 prio 3 u32 match ip tos 0x04 0xff flowid 1:3

s2 tc qdisc add dev s2-eth1 root handle 1:0 cbq avpkt 1000 bandwidth 10Mbit
s2 tc class add dev s2-eth1 parent 1:0 classid 1:1 cbq rate 3Mbit weight 1 allot 1514
s2 tc class add dev s2-eth1 parent 1:0 classid 1:2 cbq rate 5Mbit weight 2 allot 1514
s2 tc class add dev s2-eth1 parent 1:0 classid 1:3 cbq rate 2Mbit weight 3 allot 1514
s2 tc filter add dev s2-eth1 protocol ip parent 1:0 prio 1 u32 match ip tos 0x10 0xff flowid 1:1
s2 tc filter add dev s2-eth1 protocol ip parent 1:0 prio 2 u32 match ip tos 0x08 0xff flowid 1:2
s2 tc filter add dev s2-eth1 protocol ip parent 1:0 prio 3 u32 match ip tos 0x04 0xff flowid 1:3
