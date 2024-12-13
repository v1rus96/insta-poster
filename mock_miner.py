import json
import time
import requests
from config import PROXY_HOST, PROXY_PORT

def start_miner():
    # Construct the proxy URL
    proxy_url = f"http://{PROXY_HOST}:{PROXY_PORT}"
    
    try:
        while True:
            # Simulate mining data
            mining_data = {
                'worker': 'test_worker',
                'hashrate': 1000,  # 1 kH/s
                'shares': 1,
                'timestamp': int(time.time())
            }
            
            # Send mining data via HTTP POST
            try:
                response = requests.post(proxy_url, json=mining_data)
                print(f"Sent data to proxy: {mining_data}")
                
                if response.status_code == 200:
                    print(f"Received response: {response.text}")
                else:
                    print(f"Error from proxy: {response.status_code} - {response.text}")
            
            except Exception as e:
                print(f"Error sending data to proxy: {e}")
            
            # Wait before sending next update
            time.sleep(5)

    except Exception as e:
        print(f"Error in miner: {e}")

if __name__ == "__main__":
    start_miner()
