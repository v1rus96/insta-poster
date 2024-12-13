import socket
import threading
import json
import http.server
import socketserver
from config import PROXY_HOST, PROXY_PORT, POOL_HOST, POOL_PORT, modify_data

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Connect to pool
        pool_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            pool_socket.connect((POOL_HOST, POOL_PORT))
            
            # Modify and forward data to pool
            modified_data = modify_data(post_data)
            pool_socket.sendall(modified_data)
            
            # Get response from pool
            response = pool_socket.recv(4096)
            
            # Send response back to client
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response)
            
        except Exception as e:
            print(f"Error handling request: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
        finally:
            pool_socket.close()

def start_proxy():
    try:
        with socketserver.TCPServer((PROXY_HOST, PROXY_PORT), ProxyHandler) as httpd:
            print(f"Proxy server running on {PROXY_HOST}:{PROXY_PORT}, forwarding to {POOL_HOST}:{POOL_PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Error starting proxy server: {e}")

if __name__ == "__main__":
    start_proxy()
