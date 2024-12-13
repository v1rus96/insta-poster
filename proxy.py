import requests

proxy = "http://nfrvpwlvajujbee96234-zone-resi-region-kz:hayfcmmpcg@resi-as.lightningproxies.net:9999"
proxies = {"http": proxy, "https": proxy}

try:
    response = requests.get("https://www.instagram.com", proxies=proxies, timeout=5)
    print("Proxy is working:", response.status_code)
except Exception as e:
    print("Proxy failed:", e)
