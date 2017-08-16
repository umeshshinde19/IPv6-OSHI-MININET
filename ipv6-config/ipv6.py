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

ipv6 = []
dev = []
count = []
mgm_sort = []
route_addr = []
mgm_route = []
via = []
dev_route = []
subnetaddr = []


#MANAGEMENT ADDRESSES
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

#IPV6 NETWORK
print '***     Storing subnets     ***'
IPV6_file = open('./ipv6.json','r')
ipv6net = json.load(IPV6_file)
print '***-------------------------***'

for i in range(0,len(topo_ex)):
	ipv6 = ipv6 + (ipv6net[topo_ex[i]]['ipv6'])
	dev = dev + (ipv6net[topo_ex[i]]['dev'])

for i in range(0,len(topo_ex)):
	count.append(ipv6net[topo_ex[i]]['counter'])

for i in range(0,len(topo_ex)):
	for j in range(0,count[i]):
		mgm_sort.append(mgm[i])

# TOPOLOGY
topology_file = open('./topology.json','r')
topology = json.load(topology_file)

subnetaddr.append(str(topology['subnet0']))
for i in range(1,topology['counter']):
	subnetaddr.append(str(topology['subnet'+str(i)]['network'])+str(topology['subnet'+str(i)]['netmask']))

print subnetaddr

# ROUTES
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

# SSH SESSION

print '***Start SSH session and addresses & route assignment***'
# IPv6 Addresses	
for g in range(0,len(mgm_sort)):
	subprocess.Popen(['sshpass','-p',psswd,'ssh',mgm_sort[g],'sudo', 'ip', '-6', 'addr', 'add',ipv6[g],'dev',dev[g]])


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
