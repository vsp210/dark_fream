# myframework/app.py

import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from app.views import *
from app.urls import urlpatterns

class MyApp(BaseHTTPRequestHandler):
    def do_GET(self):
        for url_pattern in urlpatterns:
            if self.path == url_pattern['path']:
                response = url_pattern['view'](self)
                if response is None:
                    response = ""  # or some default response
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(response.encode())
                return
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(render(self, '404.html', templates='fream/templates').encode())

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyApp)
    print("Starting server...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
