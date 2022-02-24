#Nama  : Salsabila Martono
#NIM   : 1301194469
#Kelas : IF 43 03

from mininet.topo import Topo 
from mininet.net import Mininet 
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Link 
from mininet.node import CPULimitedHost, Node
from mininet.cli import CLI
import os

class NetworkTopo( Topo ) :
	#Membuat topologi
	def __init__(self, **oopts):
		Topo.__init__(self, **oopts)

		#inisialisasi host
		h1 = self.addHost("h1")
		h2 = self.addHost("h2")

		#inisialisasi router
		r1 = self.addHost("r1")
		r2 = self.addHost("r2")
		r3 = self.addHost("r3")
		r4 = self.addHost("r4")

		#define size bandwith
		bw1 = {"bw" : 1}		#1Mbps
		bw500 = {"bw" : 0.5}	#500Kbps

		#define size buffer
		buff = 100

		#menyambungkan antara host dan router, router dan router
		self.addLink(r1, h1, intfName1='r1-eth0', intfName2='h1-eth0', cls=TCLink, **bw1, max_queue_size=buff, use_htb=True) 		#r1-eth0 h1-eth0
		self.addLink(r1, r3, intfName1='r1-eth1', intfName2='r3-eth0', cls=TCLink, **bw500, max_queue_size=buff, use_htb=True)		#r1-eth1 r3-eth0
		self.addLink(r1, r4, intfName1='r1-eth2', intfName2='r4-eth0', cls=TCLink, **bw1, max_queue_size=buff, use_htb=True)		#r1-eth2 r4-eth0

		self.addLink(r2, h1, intfName1='r2-eth0', intfName2='h1-eth1', cls=TCLink, **bw1, max_queue_size=buff, use_htb=True)		#r2-eth0 h1-eth1
		self.addLink(r2, r3, intfName1='r2-eth1', intfName2='r3-eth1', cls=TCLink, **bw1, max_queue_size=buff, use_htb=True)		#r2-eth1 r3-eth1
		self.addLink(r2, r4, intfName1='r2-eth2', intfName2='r4-eth1', cls=TCLink, **bw500, max_queue_size=buff, use_htb=True)		#r2-eth2 r4-eth1

		self.addLink(r3, h2, intfName1='r3-eth2', intfName2='h2-eth0', cls=TCLink, **bw1, max_queue_size=buff, use_htb=True)		#h2-eth0 r3-eth2
		self.addLink(r4, h2, intfName1='r4-eth2', intfName2='h2-eth1', cls=TCLink, **bw1, max_queue_size=buff, use_htb=True)		#h2-eth1 r4-eth2

def run(): #Membuat routing
	os.system("mn -c")

	#Mulai Network
	net = Mininet(topo=NetworkTopo(), link=TCLink, host=CPULimitedHost)
	net.start()

	#Akses Topo
	h1, h2 = net.get("h1", "h2")
	r1, r2, r3, r4 = net.get("r1", "r2", "r3", "r4")

	h1.cmd("ifconfig h1-eth0 130.119.1.2/24 netmask 255.255.255.0")
	h1.cmd("ifconfig h1-eth1 130.119.4.2/24 netmask 255.255.255.0")

	h1.cmd("ip rule add 130.119.1.2 table 1")
	h1.cmd("ip rule add 130.119.4.2 table 2")
	h1.cmd("ip route add 130.119.1.0 netmask 255.255.255.0 dev h1-eth0 scope link table 1")
	h1.cmd("ip route add default via 130.119.1.1 dev h1-eth0")
	h1.cmd("ip route add 130.119.4.0 netmask 255.255.255.0 dev h1-eth1 scope link table 2")
	h1.cmd("ip route add default via 130.119.4.1 dev h1-eth1")
	h1.cmd("ip route add default scope global nexthop via 130.119.1.1 dev h1-eth0")
	h1.cmd("ip route add default scope global nexthop via 130.119.4.1 dev h1-eth1")

	h2.cmd("ifconfig h2-eth0 130.119.7.2 netmask 255.255.255.0")
	h2.cmd("ifconfig h2-eth1 130.119.8.2 netmask 255.255.255.0")
	
	h2.cmd("ip rule add 130.119.7.2 table 1")
	h2.cmd("ip rule add 130.119.8.2 table 2")
	h2.cmd("ip route add 130.119.7.0 netmask 255.255.255.0 dev h2-eth0 scope link table 1")
	h2.cmd("ip route add default via 130.119.7.1 dev h2-eth0")
	h2.cmd("ip route add 130.119.8.0 netmask 255.255.255.0 dev h2-eth1 scope link table 2")
	h2.cmd("ip route add default via 130.119.8.1 dev h2-eth1")
	h2.cmd("ip route add default scope global nexthop via 130.119.7.1 dev h2-eth0")
	h2.cmd("ip route add default scope global nexthop via 130.119.8.1 dev h2-eth1")

	r1.cmd("sysctl net.ipv4.ip_forward=1")
	r2.cmd("sysctl net.ipv4.ip_forward=1")
	r3.cmd("sysctl net.ipv4.ip_forward=1")
	r4.cmd("sysctl net.ipv4.ip_forward=1")

	r1.cmd("ifconfig r1-eth0 130.119.1.1 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth1 130.119.2.1 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth2 130.119.3.1 netmask 255.255.255.0")
	
	r1.cmd("route add -net 130.119.4.0/24 gw 130.119.3.2")
	r1.cmd("route add -net 130.119.4.0/24 gw 130.119.2.2")
	r1.cmd("route add -net 130.119.5.0/24 gw 130.119.2.2")
	r1.cmd("route add -net 130.119.6.0/24 gw 130.119.3.2")
	r1.cmd("route add -net 130.119.7.0/24 gw 130.119.2.2")
	r1.cmd("route add -net 130.119.8.0/24 gw 130.119.3.2")

	r2.cmd("ifconfig r2-eth0 130.119.4.1 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth1 130.119.5.1 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth2 130.119.6.1 netmask 255.255.255.0")

	r2.cmd("route add -net 130.119.1.0/24 gw 130.119.5.2")
	r2.cmd("route add -net 130.119.1.0/24 gw 130.119.6.2")
	r2.cmd("route add -net 130.119.2.0/24 gw 130.119.5.2")
	r2.cmd("route add -net 130.119.3.0/24 gw 130.119.6.2")
	r2.cmd("route add -net 130.119.7.0/24 gw 130.119.5.2")
	r2.cmd("route add -net 130.119.8.0/24 gw 130.119.6.2")

	r3.cmd("ifconfig r3-eth0 130.119.2.2 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth1 130.119.5.2 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth2 130.119.7.1 netmask 255.255.255.0")

	r3.cmd("route add -net 130.119.1.0/24 gw 130.119.2.1")
	r3.cmd("route add -net 130.119.3.0/24 gw 130.119.2.1")
	r3.cmd("route add -net 130.119.4.0/24 gw 130.119.5.1")
	r3.cmd("route add -net 130.119.6.0/24 gw 130.119.5.1")
	r3.cmd("route add -net 130.119.8.0/24 gw 130.119.2.1")
	r3.cmd("route add -net 130.119.8.0/24 gw 130.119.5.1")

	r4.cmd("ifconfig r4-eth0 130.119.3.2 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth1 130.119.6.2 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth2 130.119.8.1 netmask 255.255.255.0")

	r4.cmd("route add -net 130.119.1.0/24 gw 130.119.3.1")
	r4.cmd("route add -net 130.119.2.0/24 gw 130.119.3.1")
	r4.cmd("route add -net 130.119.4.0/24 gw 130.119.6.1")
	r4.cmd("route add -net 130.119.5.0/24 gw 130.119.6.1")
	r4.cmd("route add -net 130.119.7.0/24 gw 130.119.3.1")
	r4.cmd("route add -net 130.119.7.0/24 gw 130.119.6.1")

	h2.cmdPrint("iperf -s &")
	h1.cmdPrint("iperf -t 120 -c 130.119.7.2 &")

	#Mulai mininet CLI
	CLI(net)

	#network berhenti
	net.stop()


if "__main__" == __name__ :
	setLogLevel("info")
	run()