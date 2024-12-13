import socket
import json
import threading
from config import POOL_HOST, POOL_PORT

def handle_miner(client_socket):
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            
            received_data = ''
            try:
                received_data = data.decode()
                print(f"\n[POOL] Received from miner: {received_data}")
                parsed_data = json.loads(received_data)
                print(f"[POOL] Parsed JSON: {json.dumps(parsed_data, indent=2)}")
            except json.JSONDecodeError:
                print(f"[POOL] Received non-JSON data: {received_data}")
            
            # Echo the received data back
            response = {'status': 'ok', 'message': 'Share accepted'}
            response_json = json.dumps(response)
            print(f"[POOL] Sending response: {response_json}")
            client_socket.sendall(response_json.encode())
            
    except Exception as e:
        print(f"Error handling miner: {e}")
    finally:
        client_socket.close()

def start_pool():
    server_socket = None
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((POOL_HOST, POOL_PORT))
        server_socket.listen(5)
        print(f"Mock pool running on {POOL_HOST}:{POOL_PORT}")
        
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            threading.Thread(target=handle_miner, args=(client_socket,)).start()
            
    except Exception as e:
        print(f"Error in mock pool: {e}")
    finally:
        if server_socket is not None:
            server_socket.close()

if __name__ == "__main__":
    start_pool()
