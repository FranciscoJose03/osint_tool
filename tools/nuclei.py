import subprocess
import json

def run_nuclei(target):
    templates = ["http/miscellaneous/addeventlistener-detect.yaml", 
     "http/miscellaneous/apple-app-site-association.yaml", 
     "http/technologies/aws/aws-cloudfront-service.yaml", 
     "http/technologies/aws/aws-detect.yaml", 
     "dns/caa-fingerprint.yaml", 
     "http/miscellaneous/clientaccesspolicy.yaml", 
     "http/misconfiguration/cookies-without-httponly.yaml", 
     "http/misconfiguration/cookies-without-secure.yaml", 
     "http/vulnerabilities/generic/cors-misconfig.yaml", 
     "ssl/deprecated-tls.yaml", 
     "dns/dns-saas-service-detection.yaml", 
     "http/miscellaneous/email-extractor.yaml", 
     "http/technologies/fingerprinthub-web-fingerprints.yaml", 
     "http/miscellaneous/form-detection.yaml", 
     "http/exposures/tokens/google/google-api-key.yaml", 
     "http/miscellaneous/gpc-json.yaml", 
     "http/technologies/graphql-detect.yaml", 
     "dns/mx-fingerprint.yaml", 
     "dns/mx-service-detector.yaml", 
     "dns/nameserver-fingerprint.yaml", 
     "http/miscellaneous/options-method.yaml", 
     "http/miscellaneous/robots-txt.yaml", 
     "http/miscellaneous/robots-txt-endpoint.yaml", 
     "http/miscellaneous/security-txt.yaml", 
     "dns/spf-record-detect.yaml", 
     "ssl/ssl-dns-names.yaml", 
     "http/technologies/tech-detect.yaml", 
     "ssl/tls-version.yaml", 
     "http/misconfiguration/tomcat-stacktraces.yaml", 
     "dns/txt-fingerprint.yaml", 
     "http/technologies/waf-detect.yaml", 
     "ssl/wildcard-tls.yaml", 
     "http/miscellaneous/x-recruiting-header.yaml", 
     "http/misconfiguration/xss-deprecated-header.yaml"]

    command = f"nuclei -u {target} -j " + " ".join([f"-t {template}" for template in templates])

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print("Nuclei STDERR: ", result.stderr)
        return None

    return parse_nuclei_data(result.stdout)
    
def parse_nuclei_data(data):
    results = []
    for entry in data.splitlines():
        try:
            parsed_entry = json.loads(entry.strip())
            result = {
                "name": parsed_entry.get("info", {}).get("name"),
                "description": parsed_entry.get("info", {}).get("description"),
                "matched_at": parsed_entry.get("matched-at"),
                "ip": parsed_entry.get("ip"),
            }
            results.append(result)
        except json.JSONDecodeError:
            continue
    return results