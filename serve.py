#!/usr/bin/env python3
"""HTTP server with logging for Mandarin Learning Tools."""

import http.server
import socketserver
import sys
import threading
from datetime import datetime

LOG_FILE = "app_server.log"
PORT = 8000

class LogHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        client_ip = self.client_address[0]
        line = f"{timestamp} | {client_ip} | {format % args}"
        print(line)
        sys.stdout.flush()
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    
    def log_date_time_string(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f"Starting server on http://localhost:{PORT}")
print(f"Logging to {LOG_FILE}")
print("Press Ctrl+C to stop\n")

# Clear log file
open(LOG_FILE, "w").close()

with socketserver.TCPServer(("", PORT), LogHandler) as httpd:
    httpd.serve_forever()
