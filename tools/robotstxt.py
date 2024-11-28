import requests #pip install requests

def run_robots(target):
    try:
        robots_response = requests.get(f"http://{target}/robots.txt", timeout=4)
        if robots_response.status_code == 200:
            return parse_robots(robots_response.text)
        else: 
            return {}
    except Exception:
        return {}

def parse_robots(robots_txt):
    if len(robots_txt) == 0:
         return {}
    else:
        lines = robots_txt.split('\n')
        parsed_data = {"allow": [], "disallow": []}
        for line in lines:
            if line.startswith('Allow:'):
                parsed_data["allow"].append(line.split(': ')[1].strip())
            elif line.startswith('Disallow:'):
                parsed_data["disallow"].append(line.split(': ')[1].strip())
        return parsed_data