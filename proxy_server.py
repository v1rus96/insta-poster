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

        # Bi-directional data forwarding
        def forward(source, destination, modify=False):
            try:
                while True:
                    try:
                        data = source.recv(4096)
                        if not data:
                            break
                        if modify:
                            print(f"\n[PROXY] Miner -> Pool: {data.decode()}")
                            data = modify_data(data)
                            print(f"[PROXY] Modified request: {data.decode()}")
                        else:
                            print(f"\n[PROXY] Pool -> Miner: {data.decode()}")
                        destination.sendall(data)
                    except (ConnectionError, socket.error):
                        break
            except Exception as e:
                print(f"Error in forward: {e}")
            finally:
                try:
                    source.shutdown(socket.SHUT_RD)
                    destination.shutdown(socket.SHUT_WR)
                except:
                    pass

        # Start threads to handle both directions
        client_to_pool = threading.Thread(target=forward, args=(client_socket, pool_socket, True))
        pool_to_client = threading.Thread(target=forward, args=(pool_socket, client_socket))
        
        forward_threads.extend([client_to_pool, pool_to_client])
        client_to_pool.start()
        pool_to_client.start()

        # Wait for both threads to complete
        for thread in forward_threads:
            thread.join()

    except Exception as e:
        print(f"Error handling connection: {e}")
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
        proxy_socket.bind((PROXY_HOST, PROXY_PORT))
        proxy_socket.listen()
        print(f"Proxy server running on {PROXY_HOST}:{PROXY_PORT}, forwarding to {POOL_HOST}:{POOL_PORT}")
        
        while True:
            client_socket, addr = proxy_socket.accept()
            print(f"Accepted connection from {addr}")
            threading.Thread(target=handle_connection, args=(client_socket,)).start()
            
    except Exception as e:
        print(f"Error in proxy server: {e}")
    finally:
        if proxy_socket is not None:
            proxy_socket.close()

if __name__ == "__main__":
    start_proxy()
