import re

# Very small rule-based Taglish assistant. Expandable later.

INTENTS = {
    'scan': [r'(?i)scan', r'(?i)check', r'(?i)tingnan', r'(?i)scan mo'],
    'howto': [r'(?i)paano', r'(?i)how to', r'(?i)ano ang dapat'],
    'greet': [r'(?i)hi', r'(?i)hello', r'(?i)kumusta'],
    'thanks': [r'(?i)thanks', r'(?i)salamat']
}


def detect_intent(text: str):
    """Detect user intent from input text using pattern matching"""
    for intent, patterns in INTENTS.items():
        for p in patterns:
            if re.search(p, text):
                return intent
    return 'unknown'


def explain_recon(recon_result: dict):
    """Produce Taglish friendly explanation of reconnaissance results"""
    parts = []
    host = recon_result.get('host', 'unknown')
    parts.append(f"Target: {host}")

    if 'ip' in recon_result:
        parts.append(f"IP address: {recon_result['ip']}")
    else:
        parts.append("Hindi ma-resolve ang domain — siguraduhin tama ang URL.")

    if recon_result.get('uses_https'):
        parts.append("✅ Gumagamit ng HTTPS — mas secure ang koneksyon.")
    else:
        parts.append("⚠️ Hindi naka-HTTPS. I-recommend na gumamit ng SSL/TLS para secure.")

    server = recon_result.get('server') or recon_result.get('x_powered_by')
    if server:
        parts.append(f"Detected server/tech: {server}")

    if 'http_error' in recon_result:
        parts.append(f"HTTP error: {recon_result['http_error']}")

    return '\n'.join(parts)


def explain_scan_results(missing_headers, admin_pages, xss_possible):
    """Provide Taglish explanation of security scan results"""
    parts = []
    
    # Handle error cases
    if isinstance(missing_headers, dict) and 'error' in missing_headers:
        parts.append(f"Scan error: {missing_headers['error']}")
        return '\n'.join(parts)

    # Security headers analysis
    if not missing_headers:
        parts.append("✅ Security headers OK (basic check).")
    else:
        parts.append(f"⚠️ Missing security headers: {', '.join(missing_headers)}")

    # Admin pages detection
    if admin_pages:
        parts.append(f"⚠️ Nakakita ng admin/login pages: {', '.join(admin_pages)} — siguraduhin secure ang access.")

    # XSS vulnerability check
    if xss_possible:
        parts.append("⚠️ Posibleng reflected XSS (basic test). Iwasan ang mga hindi sanitized na inputs.")

    # All clear message
    if not (missing_headers or admin_pages or xss_possible):
        parts.append("🎉 Walang immediate issues na nakita sa basic checks.")

    # Provide actionable recommendations in Taglish
    parts.append('\nAction steps (madali):')
    parts.append('- Mag-install ng SSL certificate kung wala.')
    parts.append('- Gumamit ng strong passwords and limit admin access.')
    parts.append('- Update ang CMS o plugins regularly.')

    return '\n'.join(parts)
