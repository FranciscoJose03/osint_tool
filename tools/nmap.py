import nmap #pip install python-nmap

def run_nmap(ip):
    nm = nmap.PortScanner()
    try:
        return nm.scan(ip, arguments='-sV -T4 --top-ports 1')
    except Exception:
        return {}
