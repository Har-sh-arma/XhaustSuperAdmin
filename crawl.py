import netifaces
import socket
import os
import json


"Since the nmap app is used to dicover all of the devices nmap is a dependency and so is Windows findstr--> default windows filter"

selfIF = ""
index = 0


def is_port_open(host,port,timeout=2):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #presumably 
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
            selfIF = j
        



netmask = int(sum([bin(int(b)).count("1") for b in selfIF["netmask"].split(".")]))


# os.system(f"nmap -sn  {selfIF["broadcast"]}/{netmask}")
cmd_output = os.popen(f"nmap -sn  {selfIF["broadcast"]}/{netmask} | findstr \"report for *\"").read()

devices = [a.split(" ")[-1] for a in cmd_output.split("\n")]


raspis = []
for device in devices:
    if is_port_open(device, 80):
        raspis.append(device)

architecture = {"devices" : raspis}
with open('data.json', 'w') as outfile:
    json.dump(architecture, outfile)