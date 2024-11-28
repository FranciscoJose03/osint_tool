from dotenv import load_dotenv  #pip install python-dotenv --break-system-packages
import requests #pip install requests
import os

load_dotenv()
VIRUSTOTAL_API_KEY = os.getenv('VIRUS_KEY')

def run_virustotal(target):
    vt_response = requests.get(f"https://www.virustotal.com/api/v3/domains/{target}", headers={"x-apikey": VIRUSTOTAL_API_KEY})
    if vt_response.status_code == 200:
        return info_virustotal(vt_response.json())
    else:
        return {}, {}

vt_count = {
                "malicious": 0,
                "phishing": 0,
                "suspicious": 0,
                "clean": 0,
                "unrated": 0
            }

def info_virustotal(vt_data):
    if 'data' in vt_data and 'attributes' in vt_data['data'] and 'last_analysis_results' in vt_data['data']['attributes']:
                analysis_results = vt_data['data']['attributes']['last_analysis_results']    
                for result in analysis_results.values():
                    result_status = result.get('result')
                    if result_status in vt_count:
                        vt_count[result_status] += 1
    return analysis_results, vt_count

