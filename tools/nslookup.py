import subprocess

def run_nslookup(target):
    try:
        command = f"nslookup {target}"
        results = subprocess.run(command, shell=True, capture_output=True, text=True)
        return parse_nslookup(results.stdout)
    except Exception:
        return None

def parse_nslookup(data):
    try:
        ip = data.split("Non-authoritative answer:")[1].split("\n")[2].split(":")[1].split(" ")[1]
        return ip
    except Exception:
        return None