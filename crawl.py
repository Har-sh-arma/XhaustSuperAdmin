import netifaces
import socket
import os
import json
import requests
from net_tools import ping_net

"Since the nmap app is used to dicover all of the devices nmap is a dependency and so is Windows findstr--> default windows filter"

selfIF = []
index = 0





def is_port_open(host,port,timeout=0.5):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
    sock.settimeout(timeout)
    try:
       sock.connect((host,port))
    except:
       return False
    else:
       sock.close()
       return True



for interface in netifaces.interfaces():
    for i in (netifaces.ifaddresses(interface)):
        if(i!=2):
            continue
        for j in (netifaces.ifaddresses(interface)[i]):
            if (j["addr"] == "127.0.0.1"):
                continue
            selfIF.append(j)


netmasks = []
for i in selfIF:
    netmasks.append(int(sum([bin(int(b)).count("1") for b in i["netmask"].split(".")])))

# os.system(f"nmap -sn  {selfIF["broadcast"]}/{netmask}")
devices = []
for i in range(len(selfIF)):
    print(f"devices at network {selfIF[i]}")
    if(netmasks[i]<24):
        continue
    
    all_devices = ping_net(f" {selfIF[i]["addr"]}/{netmasks[i]}", 500, 20)
    devices += all_devices

print(devices)
webs = []
for device in devices:
    if device== "":
        continue
    print(f"Checking web at {device}")
    if is_port_open(device, 80):
        webs.append(device)


raspis = []
for w in webs:
    r={}
    try:
        r = requests.get(f"http://{w}/raspi", timeout=2)
        if(r.status_code == 200):
            raspis.append(w)
    except Exception as e:
        print(f"{w} : {e}")





architecture = {"devices" : raspis}
with open('data.json', 'w') as outfile:
    json.dump(architecture, outfile)