import json
import os

# Network Configuration
PROXY_HOST = '0.0.0.0'  # Bind to all interfaces
PROXY_PORT = int(os.environ.get('PORT', 8333))  # Use Render's PORT env variable or fallback to 8333

# ViaBTC Pool Configuration (using Pool 1 from the example)
POOL_HOST = 'btc.viabtc.io'
POOL_PORT = 3333  # Using the first pool port from the configuration

def modify_data(data):
    """Function to modify data (changing hashrate from 1000 to 2000)"""
    try:
        # Parse the JSON data
        json_data = json.loads(data.decode())
        
        # If there's a hashrate field and it's 1000, change it to 2000
        if 'hashrate' in json_data and json_data['hashrate'] == 1000:
            json_data['hashrate'] = 2000
            
        # Convert back to bytes
        return json.dumps(json_data).encode()
    except:
        # For Stratum protocol messages that aren't JSON, return original data
        return data
