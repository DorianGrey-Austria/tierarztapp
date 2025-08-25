#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time

class HealthHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "healthy", "service": "blender-mcp"}')
        else:
            self.send_error(404)

def start_health_server():
    server = HTTPServer(("0.0.0.0", 8080), HealthHandler)
    server.serve_forever()

if __name__ == "__main__":
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass