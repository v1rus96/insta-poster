import socket
import threading
import json
from config import PROXY_HOST, PROXY_PORT, POOL_HOST, POOL_PORT, modify_data

def handle_connection(client_socket):
    pool_socket = None
    forward_threads = []
    try:
        # Connect to the pool
        pool_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pool_socket.connect((POOL_HOST, POOL_PORT))
        print(f"[PROXY] Connected to ViaBTC pool at {POOL_HOST}:{POOL_PORT}")

        # Bi-directional data forwarding
        def forward(source, destination, source_name, dest_name, modify=False):
            try:
                while True:
                    try:
                        data = source.recv(4096)
                        if not data:
                            break
                        
                        try:
                            # Try to decode and log as JSON
                            decoded_data = data.decode()
                            print(f"\n[PROXY] {source_name} -> {dest_name}: {decoded_data}")
                            
                            if modify:
                                data = modify_data(data)
                                print(f"[PROXY] Modified data: {data.decode()}")
                            
                        except:
                            # If not JSON/decodable, log as binary
                            print(f"\n[PROXY] {source_name} -> {dest_name}: <binary data of length {len(data)}>")
                        
                        destination.sendall(data)
                    except (ConnectionError, socket.error) as e:
                        print(f"[PROXY] Connection error in {source_name} -> {dest_name}: {e}")
                        break
            except Exception as e:
                print(f"[PROXY] Error in forward {source_name} -> {dest_name}: {e}")
            finally:
                try:
                    source.shutdown(socket.SHUT_RD)
                    destination.shutdown(socket.SHUT_WR)
                except:
                    pass

        # Start threads to handle both directions
        client_to_pool = threading.Thread(
            target=forward, 
            args=(client_socket, pool_socket, "MINER", "POOL", True)
        )
        pool_to_client = threading.Thread(
            target=forward, 
            args=(pool_socket, client_socket, "POOL", "MINER", False)
        )
        
        forward_threads.extend([client_to_pool, pool_to_client])
        client_to_pool.start()
        pool_to_client.start()

        # Wait for both threads to complete
        for thread in forward_threads:
            thread.join()

    except Exception as e:
        print(f"[PROXY] Error handling connection: {e}")
    finally:
        # Clean shutdown
        try:
            if client_socket:
                client_socket.close()
            if pool_socket:
                pool_socket.close()
        except:
            pass

def start_proxy():
    proxy_socket = None
    try:
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_socket.bind((PROXY_HOST, PROXY_PORT))
        proxy_socket.listen()
        print(f"[PROXY] Server running on {PROXY_HOST}:{PROXY_PORT}")
        print(f"[PROXY] Forwarding to ViaBTC pool at {POOL_HOST}:{POOL_PORT}")
        
        while True:
            client_socket, addr = proxy_socket.accept()
            print(f"[PROXY] Accepted connection from {addr}")
            threading.Thread(target=handle_connection, args=(client_socket,)).start()
            
    except Exception as e:
        print(f"[PROXY] Error in server: {e}")
    finally:
        if proxy_socket is not None:
            proxy_socket.close()

if __name__ == "__main__":
    start_proxy()
