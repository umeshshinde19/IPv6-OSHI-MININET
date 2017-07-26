#!/usr/bin/python

import json
import subprocess
#AHAHAHAH BEL LOGO ;)
print '========================================================='
print '||                                                     ||'
print '||          __ ________  __       _  _______           ||'
print '||          || | _____ | ||      || | -----_|          ||'
print '||          || ||_____||  ||    ||  ||______           ||'
print '||          || | ______|   ||  ||   | ----- |          ||'
print '||          || ||           ||||    ||_____||          ||'
print '||          || ||            ||     |_______|          ||'
print '||                                                     ||'
print '||          Mattia Quadrini, Marco Pantanella          ||'
print '||                                                     ||'
print '========================================================='
#OPEN JSON /TMP/OVERALL_INFO
print '***Open /tmp/overall_info.json***'
with open('/tmp/overall_info.json', 'r') as overall_info:
	oinfo = json.load(overall_info)
print '***---------------------------***'

#VARIABLES
#Constraint : manual insert of hosts in the topology
topo_ex = ['peo2','peo6','cer1','cer7','cro3','cro4','cro5','ctr8']
mgm = []
psswd = '1234'
#We can modify addresses deleting names ("Subnets") and changing the "for" cycle (row 78) on the array
subnets = ['Subnet01','Subnet02','Subnet03','Subnet04','Subnet05','Subnet06','Subnet07','Subnet08','Subnet09','Subnet10','Subnet11']
hosts = []

s1= ['peo2','cer1']
s2 = ['peo2','cro4']
s3 = ['cro3','cro5']
s4 = ['peo2','cro5']
s5 = ['peo2','cro3']
s6 = ['peo6','cro3']
s7 = ['cro3','cro4']
s8 = ['peo6','cro4']
s9 = ['peo6','cro5']
s10 = ['peo6','cer7']
s11 = ['ctr8','cro3']
deb = s1+s2+s3+s4+s5+s6+s7+s8+s9+s10+s11

ipv6 = []
dev = []

#Save MGM addresses to make SSH connetction
#Open the json file and save mgm informations in mgm[]
print ''
print '***Storing MGM addresses from overall_info.json***'
for i in range(0,len(topo_ex)):
	mgm.append(str(oinfo[topo_ex[i]]['mgt_IP']))
print mgm
print ''
print '***--------------------------------------------***'
print ''

#Some Debug to show useful information
print '***Debug Info: MGM Addresses***'
print '***-------------------------***'
for i in range(0,len(mgm)):
	print topo_ex[i] + ': ' + mgm[i]
print '***-------------------------***'
print '       Example topology:       '
print topo_ex
print '***-------------------------***'

#OPEN JSON IPv6NET
#Open the IPv6 JSON file and save information about IPv6 and interfaces
print '***     Storing subnets     ***'
IPV6_file = open('./ipv6.json','r')
ipv6net = json.load(IPV6_file)
print '***-------------------------***'

#Save IPv6 addresses
#Storing hosts from JSON to array sorted according to subnets structure
print '***  Storing IPv6 addresses ***'
for i in range(0,len(subnets)):
	for j in range(len(topo_ex)):
			if topo_ex[j] in ipv6net[subnets[i]]:
				hosts.append(topo_ex[j])
#print '***          Hosts          ***'
#print hosts
print '***-------------------------***'

#Storing IPv6 Addresses from JSON to array sorted according to hosts order
j=0
while(j<len(hosts)):
	for i in range(0,len(subnets)):
		ipv6.append(str(ipv6net[subnets[i]][hosts[j]]['ipv6'].decode('unicode_escape')))
		ipv6.append(str(ipv6net[subnets[i]][hosts[j+1]]['ipv6'].decode('unicode_escape')))
		j=j+2
#print '***          IPv6           ***'
#print ipv6
#print '***-------------------------***'

#Storing Interfaces related to the own IPv6 Address from JSON to array sorted according to hosts order
z=0
while(z<len(hosts)):
	for i in range(0,len(subnets)):
		dev.append(str(ipv6net[subnets[i]][hosts[z]]['dev'].decode('unicode_escape')))
		dev.append(str(ipv6net[subnets[i]][hosts[z+1]]['dev'].decode('unicode_escape')))
		z=z+2
#print '***       Interfaces        ***'
#print dev
#print '***-------------------------***'


#Sorting MGM addresses according to subnets order. Useful to run SSH commands
print '***  Sorting MGM addresses  ***'
mgm_sort = []
for i in range(0,len(hosts)):
	for j in range(0,len(topo_ex)):
		if hosts[i].__eq__(topo_ex[j]):
			index = i
			mgm_sort.append(mgm[j])
#print mgm_sort
print '***-------------------------***'

#Open loopback6 json file
loopback6_file = open('./loopback6.json','r')
loopback6 = json.load(loopback6_file)

#Storing Loopback IPv6 addresses
#k=0
lo6 = []
for k in range(len(topo_ex)):
		lo6.append(str(loopback6[topo_ex[k]]['ipv6'].decode('unicode_escape')))
		#ipv6.append(str(loopback6[subnets[i]][hosts[k+1]]['ipv6'].decode('unicode_escape')))
		#k=k+2
#print lo6
#BASH SYNTAX
#sshpass -p $pass ssh $peo2 'sudo ip -6 addr add fd3c:9f20:5d73:01::01/64 dev vi1'

subnetaddr = ['default','fd3c:9f20:5d73:01::/64','fd3c:9f20:5d73:02::/64','fd3c:9f20:5d73:03::/64','fd3c:9f20:5d73:04::/64','fd3c:9f20:5d73:05::/64','fd3c:9f20:5d73:06::/64','fd3c:9f20:5d73:07::/64','fd3c:9f20:5d73:08::/64','fd3c:9f20:5d73:09::/64','fd3c:9f20:5d73:0a::/64','fd3c:9f20:5d73:0b::/64']
route_addr = []
mgm_route = []
via = []
dev_route = []

print '*** Sorting route addresses ***'
route_file = open('./routes.json','r')
route = json.load(route_file)

for i in range(0,len(topo_ex)):
	for j in range(0,len(subnetaddr)):
			if subnetaddr[j] in route[topo_ex[i]]:
				route_addr.append(subnetaddr[j])
				mgm_route.append(mgm[i])
				via.append(str(route[topo_ex[i]][subnetaddr[j]]['via'].decode('unicode_escape')))
				dev_route.append(str(route[topo_ex[i]][subnetaddr[j]]['dev'].decode('unicode_escape')))

print '***-------------------------***'
#print route_addr
#print mgm_route
#print via
#print dev_route

print '***Start SSH session and addresses & route assignment***'
# IPv6 Addresses
for i in range(0,len(mgm_sort)):
	ssh=subprocess.Popen(['sshpass','-p',psswd,'ssh',mgm_sort[i],'sudo', 'ip', '-6', 'addr', 'add',ipv6[i] ,'dev', dev[i]])

# IPv6 Loopback
for i in range(0,len(mgm)):
	ssh=subprocess.Popen(['sshpass','-p',psswd,'ssh',mgm[i],'sudo', 'ip', '-6', 'addr', 'add',lo6[i] ,'dev', 'lo'])

#Enable IP Forwarding
for i in range(0,len(mgm)):
	ssh=subprocess.Popen(['sshpass','-p',psswd,'ssh',mgm[i],'sudo','sysctl','-w','net.ipv6.conf.all.forwarding=1'])

# IPv6 Routing
for i in range(0,len(mgm_route)):
	ssh=subprocess.Popen(['sshpass','-p',psswd,'ssh',mgm_route[i],'sudo','ip','-6','r','add',route_addr[i],'via',via[i],'dev',dev_route[i]])
print ''
print '+=======================================================+'
print '|                Configured Successfully                |'
print '+=======================================================+'
