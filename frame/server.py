

# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import threading
#from .frame import Frame

hostName = "localhost"
serverPort = 8080

def start_server(server):
    server.serve_forever()

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

class FrameServer():    
    server = None

    def start(self):
        self.server = HTTPServer((hostName, serverPort), MyServer)
        print("Server started http://%s:%s" % (hostName, serverPort))
        threading.Thread(
            target = start_server,
            args = (self.server, )).start()

    def stop(self):
        self.server.server_close()