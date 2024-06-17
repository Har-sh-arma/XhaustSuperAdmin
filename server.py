# write the http server using Python SimpleHTTPServer base class
import http.server
import socketserver
import json
import os


system_state = None
PORT = 8000
DIRECTORY = "."




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
        # print(self.path.split("/"))
        if self.path.split("/")[1] == "data":
            with open("data.json", "r") as f:
                data = json.load(f)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
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
