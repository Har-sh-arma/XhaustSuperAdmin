'''

\r Crap is for Windows based systems should not bother on linux tho


Client service for the Reverse Proxy

tcp socket to the proxy server receives the http reqs
changes the headers to request the local server

captures response and sends it to the proxy server
'''

import socket
import re
from proxy_utils import recv_data, get_path
import argparse

SERVER_ADDR = "ec2-16-170-250-144.eu-north-1.compute.amazonaws.com"
SERVER_PORT = 1001
byte_size = 32
ASSIGNED_PATH = "/abc"
LOCAL_SERVER = "127.0.0.1"
LOCAL_PORT = 8000

parser = argparse.ArgumentParser("Client","Proxy Client for the Multi Reverse Proxy")

parser.add_argument("-p", "--path", help="path to be requested", type=str, default=ASSIGNED_PATH)
parser.add_argument("-S", "--server", help="server address", type=str, default=SERVER_ADDR)
parser.add_argument("-s", "--port", help="server port", type=int, default=SERVER_PORT)
parser.add_argument("-L", "--local", help="local server address", type=str, default=LOCAL_SERVER)
parser.add_argument("-l", "--localport", help="local server port", type=int, default=LOCAL_PORT)
parser.add_argument("-b", "--byte", help="byte size", type=int, default=byte_size)

args = parser.parse_args()

ASSIGNED_PATH = args.path
SERVER_ADDR = args.server
SERVER_PORT = args.port
LOCAL_SERVER = args.local
LOCAL_PORT = args.localport
byte_size = args.byte

# handle local server crash and re establish connection

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"Connecting to {SERVER_ADDR}:{SERVER_PORT}")
sock.connect((SERVER_ADDR, SERVER_PORT))
sock.send(b"Path:" + ASSIGNED_PATH.encode('utf-8'))
print("Connection Init")
while True:
    headers, body = recv_data(sock, (SERVER_ADDR, SERVER_PORT), byte_size)
    print("Client ⬅️ remote Server")

    try:
        detected_cookie_path =  get_path(headers)[1].encode('utf-8').removesuffix(b'\r')
    except AttributeError:
        print("❌Cookie")
    finally:
        detected_url_path = get_path(headers)[0].encode('utf-8').removesuffix(b'\r')
    detected_path = detected_url_path
    if detected_path == ASSIGNED_PATH.encode('utf-8'):
        headers = re.sub(ASSIGNED_PATH.encode('utf-8'), b"/", headers)

    local_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_sock.connect((LOCAL_SERVER, LOCAL_PORT))
    local_sock.send(headers + body)
    print("local server ⬅️ Client")
    
    resp_headers, resp_body = recv_data(local_sock, (LOCAL_SERVER, LOCAL_PORT), byte_size)
    local_sock.close()
    print("local server ➡️ Client")
    
    resp = resp_headers + resp_body
    sock.send(resp)
    print("Client ➡️ remote Server")


