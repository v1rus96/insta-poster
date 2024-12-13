import socket
import threading
import json

# Configuration for Proxy
PROXY_HOST = '127.0.0.1'  # Proxy server address
PROXY_PORT = 8333         # Proxy server port
POOL_HOST = '127.0.0.1'   # Mock pool address
POOL_PORT = 8334          # Mock pool port

# Function to handle communication between miner and pool
def handle_connection(client_socket):
    pool_socket = None
    try:
        # Connect to the pool
        pool_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pool_socket.connect((POOL_HOST, POOL_PORT))

        # Bi-directional data forwarding
        def forward(source, destination, modify=False):
            while True:
                data = source.recv(4096)
                if not data:
                    break
                if modify:
                    data = modify_data(data)
                destination.sendall(data)

        # Start threads to handle both directions
        threading.Thread(target=forward, args=(client_socket, pool_socket)).start()
        threading.Thread(target=forward, args=(pool_socket, client_socket, True)).start()

    except Exception as e:
        print(f"Error handling connection: {e}")
    finally:
        client_socket.close()
        if pool_socket:
            pool_socket.close()

# Function to modify data (inflating hash rate in this example)
def modify_data(data):
    try:
        # Decode Stratum JSON messages
        message = json.loads(data.decode('utf-8'))
        if message.get("method") == "mining.submit":
            print(f"Original Data: {message}")
            # Simulate inflated hash rate or modify parameters
            message["params"][3] = "inflated_nonce_value"
            print(f"Modified Data: {message}")
            return json.dumps(message).encode('utf-8')
    except Exception as e:
        print(f"Failed to modify data: {e}")
    return data

# Start the proxy server
def start_proxy():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((PROXY_HOST, PROXY_PORT))
    proxy_socket.listen(5)
    print(f"Proxy server running on {PROXY_HOST}:{PROXY_PORT}, forwarding to {POOL_HOST}:{POOL_PORT}")

    while True:
        client_socket, addr = proxy_socket.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_connection, args=(client_socket,)).start()

if __name__ == "__main__":
    start_proxy()

# Mock Miner Script
def mock_miner():
    MOCK_MINER_HOST = '127.0.0.1'
    MOCK_MINER_PORT = 8333
    client_socket = None
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((MOCK_MINER_HOST, MOCK_MINER_PORT))
    except Exception as e:
        print(f"Failed to connect to the mock miner: {e}")
        return  # Exit the function if connection fails

    message = {
        "id": 4,
        "method": "mining.submit",
        "params": ["worker1", "job_id", "nonce", "hash"]
    }
    print(f"Mock Miner Sending: {message}")
    if client_socket:
        client_socket.sendall(json.dumps(message).encode('utf-8'))

        response = client_socket.recv(4096)
        if response:
            print(f"Response from Proxy: {response.decode('utf-8')}\n")

    if client_socket:
        client_socket.close()

# Mock Pool Script
def mock_pool():
    MOCK_POOL_HOST = '127.0.0.1'
    MOCK_POOL_PORT = 8334
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((MOCK_POOL_HOST, MOCK_POOL_PORT))
        server_socket.listen(5)
        print(f"Mock Pool running on {MOCK_POOL_HOST}:{MOCK_POOL_PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Mock Pool Connection from {addr}")
            data = client_socket.recv(4096)
            if data:
                print(f"Mock Pool Received Data: {data.decode('utf-8')}")

    except Exception as e:
        print(f"Error in mock pool: {e}")

# To Test:
# Run `mock_pool` first, then `start_proxy`, and finally `mock_miner`
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python script.py [mock_pool | start_proxy | mock_miner]")
    elif sys.argv[1] == "mock_pool":
        mock_pool()
    elif sys.argv[1] == "start_proxy":
        start_proxy()
    elif sys.argv[1] == "mock_miner":
        mock_miner()
    else:
        print("Invalid option. Use mock_pool, start_proxy, or mock_miner.")
