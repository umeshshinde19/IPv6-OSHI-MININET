#!/bin/python
#PINGv6 TEST
import subprocess

ipv6net = 'fd3c:9f20:5d73'
subnet = ['1','2','3','4','5','6','7','8','9','a','b']
padding = '::'
device = ['1','2']
debug = 0
for i in range(0,len(subnet)):
	print "||-----------------PING"+str(i+1)+"-----------------||"
	for j in range(0, len(device)):
		ping = subprocess.Popen(['ping6','-c','1',ipv6net+':'+subnet[i]+padding+device[j]],stdout=subprocess.PIPE)
		out = ping.communicate()[0]
		print out
		print ""
	print ""