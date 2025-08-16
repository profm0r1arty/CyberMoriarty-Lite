import socket
import requests
from urllib.parse import urlparse


def get_hostname_from_input(url_or_domain):
    """Extract hostname from URL or domain input"""
    if not url_or_domain.startswith('http'):
        url = 'http://' + url_or_domain
    else:
        url = url_or_domain
    parsed = urlparse(url)
    return parsed.netloc


def recon(url_or_domain, timeout=5):
    """
    Return basic reconnaissance information including:
    - IP address resolution
    - HTTP response details
    - Security indicators (HTTPS usage)
    - Server/technology detection
    """
    host = get_hostname_from_input(url_or_domain)
    result = {'host': host}
    
    # DNS resolution
    try:
        ip = socket.gethostbyname(host)
        result['ip'] = ip
    except Exception as e:
        result['ip_error'] = str(e)

    # HTTP reconnaissance
    try:
        # Try HTTP first
        r = requests.get(('http://' + host), timeout=timeout, allow_redirects=True)
        result['final_url'] = r.url
        result['status_code'] = r.status_code
        
        # Extract useful headers for security analysis
        headers = r.headers
        result['server'] = headers.get('Server')
        result['x_powered_by'] = headers.get('X-Powered-By')
        result['content_type'] = headers.get('Content-Type')
        
        # Check if redirected to HTTPS
        result['uses_https'] = r.url.startswith('https://')
        
    except Exception as e:
        result['http_error'] = str(e)
        
        # Try HTTPS if HTTP failed
        try:
            r = requests.get(('https://' + host), timeout=timeout, allow_redirects=True)
            result['final_url'] = r.url
            result['status_code'] = r.status_code
            result['uses_https'] = True
            
            headers = r.headers
            result['server'] = headers.get('Server')
            result['x_powered_by'] = headers.get('X-Powered-By')
            result['content_type'] = headers.get('Content-Type')
            
        except Exception as e2:
            result['https_error'] = str(e2)

    return result
