import requests #pip install requests

def run_iplocation(ip):
    try:
        ip_response = requests.get(f"http://ip-api.com/json/{ip}")
        if ip_response.status_code == 200:
            return ip_response.json() 
        else:
            return {}
    except Exception:
        return {}