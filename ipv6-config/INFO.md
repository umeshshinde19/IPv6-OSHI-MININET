## Instructions

Edit ipv6.json as follow:  
`{"HOST":{"counter" : 5, "ipv6": ["ADDRESSES"],"dev": ["DEVICES"]}}`  

 - HOST = the name of the host in the topology  
 - counter = number of ADDRESSES and DEVICES (must be the same)  
 - ADDRESSES = list of IPv6 addresses to assign  
 - DEVICES = list of devices according to the related ipv6 address to be assigned  

Let's sort ADDRESSES and DEVICES arrays according to the order, for example:  
 - ADDRESSES[i] is the IPv6 address to be assigned to the interface DEVICES[i] 
 
## ipv6.json
This file contains the IPv6 addresses and the interfaces related to the addresses for each host.  
If the topology changes this file has to be changed according to the topology in terms of:  
 - Name of each host
 - IPv6 addresses of each host
 - Interfaces related to each IPv6 address of each host
 
## routes.json
Like _ipv6.json_ this file contain the list of the routes to add to each host

`{"peo2":{"ROUTE":{"via": "NEXT_HOP_ADDRESS","dev": "DEVICE_TO_NEXT_HOP"}}}`  
 - ROUTE = the route to add  
 - NEXT_HOP_ADDRESS = the address of the next hop
 - DEVICE_TO_NEXT_HOP = the host interface to NEXT_HOP_ADDRESS

 ## topology.json
This file contains the description of the desired topology of the network:

`{"counter":VALUE,"subnet0":"default","subnet(i)":{"network":"NET_ADDRESS","netmask":"NET_VALUE"}}`

 - VALUE = number of the subnets  
 - SUBNET0 has to be keeped  
 - (i) = number of the subnet  
 - NET_ADDRESS = network address without netmask  
 - NET_VALUE = "/netmask"

This file has to be changed according to the topology of the network.
 
 