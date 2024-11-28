import requests #pip install requests

def check_target(url):
    try:
        response = requests.get(f"http://{url}")
        if response.status_code:
            return True, None
    except requests.exceptions.RequestException as e:
        return False, parse_web_error(str(e))

def parse_web_error(error): #HTTPConnectionPool(host='XXX.XXX', port=XXX): Max retries exceeded with url: / (Caused by NameResolutionError("<urllib3.connection.HTTPConnection object at 0x000000>: Failed to resolve 'XXX.XXX' ([Errno -2] Name or service not known)"))
    a = error.split(": ")[3] #Failed to resolve 'XXX.XXX' ([Errno -2] Name or service not known)"))
    b = a.split(' (')[0] #Failed to resolve 'XXX.XXX'
    c = a.split('] ')[1].split(')')[0] #Name or service not known
    parse_web_error = f"{b}<br/>{c}" #Failed to resolve 'XXX.XXX' salto Name or service not known
    return parse_web_error