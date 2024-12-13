import socket
import json
import time
from config import PROXY_HOST, PROXY_PORT

def start_miner():
    client_socket = None
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((PROXY_HOST, PROXY_PORT))
        print(f"Connected to proxy at {PROXY_HOST}:{PROXY_PORT}")
        
        # Simulate mining by sending periodic updates
        while True:
            # Simulate mining data
            mining_data = {
                'worker': 'test_worker',
                'hashrate': 1000,  # 1 kH/s
                'shares': 1,
                'timestamp': int(time.time())
            }
            
            # Send mining data
            client_socket.sendall(json.dumps(mining_data).encode())
            
            # Receive response
            response = client_socket.recv(4096)
            if response:
                print(f"Received response: {response.decode()}")
            
            # Wait before sending next update
            time.sleep(5)
            
    except Exception as e:
        print(f"Error in mock miner: {e}")
    finally:
        if client_socket:
            client_socket.close()

if __name__ == "__main__":
    start_miner()
