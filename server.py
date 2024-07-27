# write the http server using Python SimpleHTTPServer base class
import http.server
import socketserver
import json
import os
from fork_util import fork_list, kill_all
import argparse

system_state = None
PORT = 8000
DIRECTORY = "."


parser = argparse.ArgumentParser("Crawler","Crawler to Discover Raspis on the Network")

parser.add_argument("-p", "--path", help="Path for the parent Superadmin", type=str, default="/abc")
parser.add_argument("-P", "--port", help="Port for the parent Superadmin", type=int, default=1001)
parser.add_argument("-S", "--server", help="server address", type=str)

args = parser.parse_args()


pid_list = []

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
   
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(Handler, self).end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()


    #add a get method to serve when super returns 404 (not found)
    def do_GET(self):
        global pid_list
        # print(self.path.split("/"))
        if self.path.split("/")[1] == "data":
            with open("data.json", "r") as f:
                data = json.load(f)
            kill_all(pid_list)
            
            remote_ports = []
            for i in range(len(data["devices"])):
                remote_ports.append(args.port+i+1)
            data["remote_ports"]= remote_ports
            pid_list = fork_list(data["devices"], remote_ports, args.server, 80, args.path)
            self.send_response(200)
            body = json.dumps(data).encode()
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(body))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path.split("/")[1] == "sync":
            os.system("py crawl.py")
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
            return
        super().do_GET()
        return
    
    # def do_POST(self):

    #     self.send_response(200)
    #     self.end_headers()
    #     return



if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever(0.5)
