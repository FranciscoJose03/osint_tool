import requests #pip install requests
import re

def run_wayback(target):
    
    waym_results = []
    try:
        waym_request = requests.get(f"https://web.archive.org/cdx/search/cdx?url={target}/*&output=json&collapse=urlkey&fl=original&limit=1")
        waym_all = re.findall(r'(http[s]?://[^"]+)', waym_request.text)
        for url in waym_all:
            status = status_code_website(url)
            wayback_url = {
                "url": url,
                "status": status
            }
            waym_results.append(wayback_url)
            return waym_results
    except Exception:
        return waym_results

def status_code_website(url):
    try:
        response = requests.get(f"http://web.archive.org/web/{url}")
        return response.status_code
    except Exception:
        return None
