# Mattia's README file

***
# Test using Bash commands
## Introduction  
_First approach was the insert of IPv6 addresses via bash. According to the _IPv6_Manual_Strucure_
file I made SSH connection using MGM addresses from Linux machine to VMs and then I added IPv6 addresses to every machine. Finally I tested PP link between each Subnet
with ping6 command_



## BASH Command List
##### SSH to VMs
 - `ssh <mgm_address>`  
 - `VMs SSH password = "1234"`
 - `sudo su`

> Usually I obtain **su** rights to run some commands like **ip**.  
> SSH connection are made according to Management addresses listed in the _IPv6_Manual_Strucure_ file
taken from the _Deploymet_Example_OUT_ file.  

##### Adding new IPv6 address  
 - `ip -6 addr add <ip6address>/<length> dev <device>`

##### Removing existing IPv6 address  
 - `ip -6 addr del <ip6address>/<length> dev <device>`

##### Ping an IPv6 device
 - `ping6 <ip6address>`



## Procedure and comments
 1. Make SSH connection to every machine in the OSHI_Example_Project  
 - `ssh 10.255.255.1`  **cro5**  
 - `ssh 10.255.254.1`  **cro3**  
 - `ssh 10.255.253.1`  **cro4**  
 - `ssh 10.255.252.1`  **peo2**  
 - `ssh 10.255.251.1`  **peo6**  
 - `ssh 10.255.250.1`  **cer1**  
 - `ssh 10.255.249.1`  **cer7**  
 - `ssh 10.255.248.1`  **ctr8**  

 2. According to the IPv6 Structure proposed let's assign IPv6 addresses to VMs. Make attention to assign the address to the correct interface. According to the IPv4 topology we can assign IPv6 addresses to the same IPv4 interfaces such that we can support IPv6 to IPv4.  
 - `ip -6 addr add fd3c:9f20:5d73:01::01/64 dev vi1`  **peo2** on Subnet1  
 - `ip -6 addr add fd3c:9f20:5d73:01::02/64 dev cer1-eth1`  **cer1** on Subnet1 

 3. If I add a **new IPv6 address**, the system automatically creates the route for the network  
 - `ip -6 route show`  **peo2**  
 - `fd3c:9f20:5d73:1::/64 dev vi1  proto kernel  metric 256`  
 
 4. To fully support OSHI_Example to IPv6 we can add also MGM IPv6 addresses  
 - `ip -6 addr add fd3c:9f20:5d73:ffff::01/64 dev vi0`  **cro5**  
 - (...)
 
 5. Adding IPv6 to VMs we have to add IPv6 also to our Linux machine  
 - `ip -6 addr add fd3c:9f20:5d73:ffff::02/64 dev eth0`  
 - (...)  

 6. Ping in each PP Subnet using IPv6  
 - `ping6 fd3c:9f20:5d73:01::01` from **cer1** to **peo2**  
 - (...)

 7. Adding loopback IPv6 address to _lo_ interface  
 - `ip -6 addr add <address>/128 dev lo`  
 - LO addresses are chosen according to the _IPv6_Manual_Structure file_


## Automatic allocation of IPv6 addresses

Using this script _MQ_ipv6_ssh_address.sh_ for the OSHI_Example_Project I can execute automatically commands described above.  
The script uses  

`sshpass -p <password>`  

to connect using ssh to the target VM without asking the password known a priori; 
then I concatenated the command  

`ssh <address> <command>`  

to give IPv6 address to the target VM; for example  

`pass=1234`  
`peo2="10.255.252.1"`  
`sshpass -p $pass ssh $peo2 'sudo ip -6 addr add fd3c:9f20:5d73:01::01/64 dev vi1'`

The script also automatic assign LO IPv6 addresses to each VM

`sshpass -p $pass ssh $cro4 'sudo ip -6 addr add fdac::03/128 dev lo'`

***

# SSH Using Python 

## Introduction 
I rearranged the work made using bash commands in a python file that reads information from JSON files and makes SSH connection to assign IPv6 addresses.


## Procedure
1. I created a Python script that takes informations about topology from _overall_info.json_ placed in the _/tmp_ folder  
 - MGM addresses useful to make SSH connections  

2. I takes other information about IPv6 addresses to be assigned to each host from _ipv6.json_ made by myself and that contains _Subnets_ and the structure of the _IPv6 Network_  
 - IPv6 Addresses  
 - Interfaces  

3. I collected and I sorted following informations into some arrays  
 - Topology hosts _(pair of hosts each in the related subnet)_
   - E.G. _(peo2,cer1,peo2,cro4,...)_
 - MGM addresses of related hosts
   - E.G. _(10.255.252.1, 10.255.250.1, 10.255.252.1, 10.255.253.1, ...)_
 - IPv6 addresses of related hosts
 - Interfaces of related hosts  
   Arrays are sorted such that the index [i] of any array is related to the same host:  
   IPv6[i] - DEV[i] - MGM[i] are related all to hosts[i]
 
 
4. In this way I could make SSH operation using _subprocess_ with one single command in a _for_ cycle :  

`for i in range(0,len(mgm_sort)):
	ssh=subprocess.Popen(['sshpass','-p',psswd,'ssh',mgm_sort[i],'sudo', 'ip', '-6', 'addr', 'add',ipv6[i] ,'dev', dev[i]])`


5. The same it is done about Loopback IPv6 addresses.

`for i in range(0,len(mgm)):
	ssh=subprocess.Popen(['sshpass','-p',psswd,'ssh',mgm[i],'sudo', 'ip', '-6', 'addr', 'add',lo6[i] ,'dev', 'lo'])`

#### Comments

To make SSH connection it is use Python library _subprocess_
`shell=subprocess.Popen(['command','parameter','parameter'])`
***
# References  
 - [Deployment_Example_OUT](https://bitbucket.org/nip1617/ipv6-oshi-grpc/src/eea8669a79af1ee77b0258a44db807d3287eb8ce/ipv6/Deployment_OUT.txt?at=master)
 - [IPv6_Structure](https://bitbucket.org/nip1617/ipv6-oshi-grpc/src/eea8669a79af1ee77b0258a44db807d3287eb8ce/ipv6/IPv6_Structure.txt?at=master)
 - [IPv6 Private Addresses Structure](http://simpledns.com/private-ipv6.aspx)
 - [RFC4193](http://www.rfc-editor.org/rfc/rfc4193.txt)

# Setup  
 - [MQ_ipv6_ssh_address.sh](https://bitbucket.org/nip1617/ipv6-oshi-grpc/src/eea8669a79af1ee77b0258a44db807d3287eb8ce/ipv6/MQ_ipv6_ssh_address.sh?at=master)
 - [IPv6.py](https://bitbucket.org/nip1617/ipv6-oshi-grpc/src/eea8669a79af1ee77b0258a44db807d3287eb8ce/ipv6/ipv6.py?at=master)
 - [Subnets.json](https://bitbucket.org/nip1617/ipv6-oshi-grpc/src/eea8669a79af1ee77b0258a44db807d3287eb8ce/ipv6/ipv6.json?at=master)
 - [LoopbackIPv6.json](https://bitbucket.org/nip1617/ipv6-oshi-grpc/src/eea8669a79af1ee77b0258a44db807d3287eb8ce/ipv6/loopback6.json?at=master)
 - [pingv6.py](https://bitbucket.org/nip1617/ipv6-oshi-grpc/src/4c223dda36a1b639785a0f3e4db3d5553196ce17/ipv6/pingv6.py?at=master)
****
# OSHI Example Topology
![OSHI_Example](https://bytebucket.org/nip1617/ipv6-oshi-grpc/raw/47e92648c943342635e0dbcfaa2c5edc1ed10fec/ipv6/media/OSHI_SUB.jpg?token=756d566ef420f40fa81e663e1b81db83b55ea08f)  
