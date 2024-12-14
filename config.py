import json
import os

# Network Configuration
PROXY_HOST = '0.0.0.0'  # Bind to all interfaces
PROXY_PORT = 8333

POOL_HOST = 'ltc.viabtc.io'
POOL_PORT = 3333

# Set extremely low difficulty to generate many more shares
TARGET_DIFFICULTY = 0.000000001  # Lowered 100x from original 0.01

def modify_data(data):
    """Function to modify data and adjust difficulty for more shares"""
    try:
        # Parse the JSON data
        decoded = data.decode()
        if not decoded.endswith('\n'):
            decoded += '\n'
        
        json_data = json.loads(decoded)
        
        if isinstance(json_data, dict):
            # Handle difficulty setting
            if json_data.get('method') == 'mining.set_difficulty':
                print(f"[PROXY] Original difficulty: {json_data['params'][0]}")
                json_data['params'][0] = TARGET_DIFFICULTY
                print(f"[PROXY] Setting difficulty to: {TARGET_DIFFICULTY}")
        
        # Convert back to bytes and ensure it ends with newline
        return (json.dumps(json_data) + '\n').encode()
    except Exception as e:
        print(f"[PROXY] Error in modify_data: {e}")
        return data
