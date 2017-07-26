# Marco Pantanella - README

 ***   

## Assegnazione delle rotte

Per l'assegnazione delle rotte, si consideri la figura seguente, rappresentante la topologia di rete: 

![topology](https://bytebucket.org/nip1617/ipv6-oshi-grpc/raw/c6cd8ec6449792d6d034424071a7603835e1ad9c/ipv6/media/topologia.jpg?token=b0a16ce415c94493daf86e5e59310a50a8febf77)

basata sulla struttura e gli indirizzi IPv6 indicati nel file: [IPv6 Structure](https://bitbucket.org/nip1617/ipv6-oshi-grpc/raw/88e4668e8ce806db0f1f309bdafcb972522f7891/ipv6/IPv6_Structure.txt).

Ho creato inizialmente un script **JSON** ([routes.json](https://bitbucket.org/nip1617/ipv6-oshi-grpc/raw/88e4668e8ce806db0f1f309bdafcb972522f7891/ipv6/routes.json)) che indica per ogni gateway la rotta di default e le rotte alternative da me stabilite e contiene per ognuna di esse le variabili _via_ e _dev_.
Successivamente abbiamo implementato uno script ***_python_***  ([IPv6.py](https://bitbucket.org/nip1617/ipv6-oshi-grpc/raw/88e4668e8ce806db0f1f309bdafcb972522f7891/ipv6/ipv6.py)) che assegna gli indirizzi IPv6 e le rotte in base ai corrispettivi file _JSON_ ([address.json](https://bitbucket.org/nip1617/ipv6-oshi-grpc/raw/88e4668e8ce806db0f1f309bdafcb972522f7891/ipv6/ipv6.json)) e ([routes.json](https://bitbucket.org/nip1617/ipv6-oshi-grpc/raw/88e4668e8ce806db0f1f309bdafcb972522f7891/ipv6/routes.json)). 
Prima di fare cio', vengono creati gli array per gli indirizzi di management, per gli indirizzi delle rotte di destinazione e infine per le interfacce (_via_) e i device (_dev_), con la seguente relazione:

    for i in range(0,len(topo_ex)):
	for j in range(0,len(subnetaddr)):
			if subnetaddr[j] in route[topo_ex[i]]:
				route_addr.append(subnetaddr[j])
				mgm_route.append(mgm[i])
		        via.append(str(route[topo_ex[i]][subnetaddr[j]]['via'].decode('unicode_escape')))
				dev_route.append(str(route[topo_ex[i]][subnetaddr[j]]['dev'].decode('unicode_escape')))

dove: 

- `subnetddr = ['default','fd3c:9f20:5d73:01::/64','fd3c:9f20:5d73:02::/64','fd3c:9f20:5d73:03::/64','fd3c:9f20:5d73:04::/64','fd3c:9f20:5d73:05::/64','fd3c:9f20:5d73:06::/64','fd3c:9f20:5d73:07::/64','fd3c:9f20:5d73:08::/64','fd3c:9f20:5d73:09::/64','fd3c:9f20:5d73:0a::/64','fd3c:9f20:5d73:0b::/64']`
 contiene gli indirizzi di tutte le subnet
 
- `topo_ex = ['peo2','peo6','cer1','cer7','cro3','cro4','cro5','ctr8']`
contiene i nodi della topologia di rete presa in considerazione

vengono dunque confrontati gli indirizzi delle subnet in subnetddr con gli indirizzi delle rotte di destinazione per ogni nodo nel file json routes.json e se presenti, vengono estrapolati i dati necessari per creare gli array:

- _mgm_route_ : contenente gli indirizzi di management per la connessione _ssh_
- _route_addr_: contenente gli indirizzi delle rotte di destinazione
- _via_: contenente gli indirizzi delle rotte di passaggio
- _dev_: contenente i device di uscita dai gateway

## SSH SESSION

Infine per assegnare le rotte, viene stabilita una connessione **SSH** su ogni _Virtual Machine_ , dove viene prima abilitato l' _IPv6 Forwarding_ con il seguente comando:

    sudo sysctl -w net.ipv6.conf.all.forwarding=1

Successivamente vengono utilizzati nel seguente ciclo _for_ gli array precedentemente ricavati:

    for i in range(0,len(mgm_route)):
	    ssh=subprocess.Popen(['sshpass','-p',psswd,'ssh',mgm_route[i],'sudo','ip','-6','r','add',route_addr[i],'via',via[i],'dev',dev_route[i]])
a questo punto, ogni nodo della rete avra' le rotte stabilite nel file _routes.json_ e viene confermato all'utente l'avvenuta configurazione con il messaggio "_configured successfully_". 

#### Commenti
Per instaurare connessioni SSH in python è stata usata la libreria _subprocess_
`shell=subprocess.Popen(['command','parameter','parameter'])`

