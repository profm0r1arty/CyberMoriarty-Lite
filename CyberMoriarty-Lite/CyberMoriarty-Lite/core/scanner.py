import requests
from urllib.parse import urljoin

# Common administrative interface paths
COMMON_ADMIN_PATHS = [
    '/admin', 
    '/login', 
    '/administrator', 
    '/user/login', 
    '/wp-admin',
    '/admin.php',
    '/login.php',
    '/admin/login',
    '/management',
    '/control-panel'
]

# Important security headers that should be present
SECURITY_HEADERS = [
    'X-Frame-Options', 
    'Content-Security-Policy', 
    'X-Content-Type-Options', 
    'Strict-Transport-Security',
    'X-XSS-Protection'
]


def check_security_headers(url_or_domain, timeout=5):
    """
    Check for missing security headers that help protect against
    common web vulnerabilities like clickjacking, XSS, etc.
    """
    host = url_or_domain
    if not host.startswith('http'):
        host = 'http://' + host
        
    try:
        r = requests.get(host, timeout=timeout, allow_redirects=True)
        missing = [h for h in SECURITY_HEADERS if h not in r.headers]
        return missing
    except Exception as e:
        return {'error': str(e)}


def find_admin_pages(url_or_domain, timeout=3):
    """
    Discover common administrative interfaces that may be
    exposed and require proper access controls
    """
    host = url_or_domain
    if not host.startswith('http'):
        host = 'http://' + host
        
    found = []
    for path in COMMON_ADMIN_PATHS:
        try:
            url = urljoin(host, path)
            r = requests.get(url, timeout=timeout, allow_redirects=False)
            
            # Consider various success indicators
            if r.status_code in [200, 302, 301]:
                found.append(path)
                
        except requests.exceptions.RequestException:
            # Continue checking other paths even if one fails
            continue
            
    return found


def quick_xss_reflection_test(url_or_domain, timeout=5):
    """
    Basic reflected XSS test using a simple payload.
    This is a minimal test - comprehensive XSS testing requires more sophisticated approaches.
    """
    host = url_or_domain
    if not host.startswith('http'):
        host = 'http://' + host
        
    # Simple test payload that's unlikely to cause harm
    payload = "<s1>moriarty_test</s1>"
    
    try:
        # Test with common parameter names
        test_params = ['q', 'search', 'query', 'input', 'test']
        
        for param in test_params:
            try:
                r = requests.get(host, params={param: payload}, timeout=timeout)
                if payload in r.text:
                    return True
            except requests.exceptions.RequestException:
                continue
                
    except Exception:
        pass
        
    return False


def port_scan_common(host, timeout=2):
    """
    Basic port scanning for common services.
    Limited to avoid being too aggressive or triggering security systems.
    """
    import socket
    
    if host.startswith('http'):
        from urllib.parse import urlparse
        parsed = urlparse(host)
        host = parsed.netloc
    
    # Common ports to check
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
    open_ports = []
    
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except Exception:
            continue
            
    return open_ports
