import multiprocessing
import os
# Define a function that takes in a list of Local IP adresses in a list as input and creates a fork corresponding to each IP return pid list

def fork_list(ip_list: list, remote_ports: list, remote_addr: str , local_port: int=80, superadmin_path: str="/abc")-> list:
    p_list = []
    for i in range(len(ip_list)):
        p = multiprocessing.Process(target=client, args=(ip_list[i], remote_ports[i], remote_addr, local_port, superadmin_path))
        p.start()
        p_list.append(p)
    return p_list

def client(ip, remote_port, remote_addr, local_port, superadmin_path):
    os.system(f".venv\\Scripts\\python.exe ProxyClient\\client.py -p {superadmin_path+str(remote_port)} -S {remote_addr} -s {remote_port} -L {ip} -l {local_port}")
    

def kill_all(p_list: list):
    for i in p_list:
        i.kill()
        


