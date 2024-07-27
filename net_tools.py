#a python script to ping all th hosts on a network using n number of parallel threads

import threading
import time
from queue import Queue
import subprocess
import time



#loop through all the possible ips in the subnet
devices = []

def base2(a):
    return bin(int(a))


def toBin(ip):
    network_ip_list = list(map(base2, ip.split(".")))
    cat_string= "".join(network_ip_list).replace("0b", "")
    return cat_string

def toIP(b_string):
    return ".".join([str(int(b_string[i:i+8], 2)) for i in range(0, len(b_string), 8)])

class pinger(threading.Thread):
    def __init__(self, q: Queue, print_lock : threading.Lock, wait: int =10):
        threading.Thread.__init__(self)
        self.q = q
        self.print_lock = print_lock
        self.wait = wait

    def run(self):
        global devices
        while not self.q.empty():
            ip = self.q.get()
            cmd = f"ping {ip} -n 1 -w {self.wait}"
            out = subprocess.getoutput(cmd)
            if("Received = 1" in out):
                self.print_lock.acquire()
                # print(out)
                devices.append(ip)
                self.print_lock.release()
            self.q.task_done()









def ping_net(networkAddr: str, n: int, wait: int = 10):
    global devices
    mask = int(networkAddr.split("/")[1])
    queue_list = []
    for i in range(n):
        queue_list.append(Queue())
    cat_string = toBin(networkAddr.split("/")[0])
    cat_string = cat_string[:mask] + "0" * (32 - mask)
    MasK_xor = pow(2, 32 - mask)

    i = 0
    while(True):
        curr_val = int(cat_string, 2) + 1
        prev_value = int(cat_string, 2)
        if(curr_val ^ prev_value > MasK_xor):
            break
        cat_string = bin(curr_val).replace("0b", "")
        queue_list[i % n].put(toIP(cat_string))
        i+=1
    t_list = []
    print_lock = threading.Lock()
    for i in range(n):
        t = pinger(queue_list[i], print_lock, wait)
        t_list.append(t)
        t.start()
        
    for t in t_list:
        t.join()
    return devices





if __name__ == "__main__":
    n = 500
    networkAddr = "192.168.240.255/24"
    start_time = time.time()
    print(ping_net(networkAddr, n))
    end_time = time.time()
    print(end_time - start_time)

