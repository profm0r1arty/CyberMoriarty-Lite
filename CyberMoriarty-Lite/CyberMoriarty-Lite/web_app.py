#!/usr/bin/env python3
"""
CyberMoriarty Lite - Web Interface
A web-based cybersecurity reconnaissance tool with Taglish assistant interface
"""

from flask import Flask, render_template, request, jsonify
import threading
import json
from core.recon import recon
from core.scanner import check_security_headers, find_admin_pages, quick_xss_reflection_test
from assistant import detect_intent, explain_recon, explain_scan_results

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_endpoint():
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'Kulang ang URL'}), 400
    
    try:
        # Run all scans
        scan_result = run_full_scan(url)
        return jsonify(scan_result)
        
    except Exception as e:
        return jsonify({'error': f'Scan error: {str(e)}'}), 500

def run_full_scan(url):
    """Run comprehensive security scan"""
    results = {
        'url': url,
        'status': 'scanning',
        'timestamp': None
    }
    
    # Run reconnaissance
    recon_data = recon(url)
    
    # Run security checks
    missing_headers = check_security_headers(url)
    admin_pages = find_admin_pages(url)
    xss_test = quick_xss_reflection_test(url)
    
    # Generate explanations
    recon_explanation = explain_recon(recon_data)
    security_explanation = explain_scan_results(missing_headers, admin_pages, xss_test)
    
    results.update({
        'status': 'completed',
        'recon': {
            'data': recon_data,
            'explanation': recon_explanation
        },
        'security': {
            'missing_headers': missing_headers,
            'admin_pages': admin_pages,
            'xss_possible': xss_test,
            'explanation': security_explanation
        }
    })
    
    return results

@app.route('/help')
def help_endpoint():
    help_info = {
        'title': 'CyberMoriarty Lite Help',
        'description': 'Cybersecurity scanner na gawa para sa mga Filipino security practitioners',
        'features': [
            'DNS resolution at IP lookup',
            'HTTPS/SSL status checking', 
            'Security headers analysis',
            'Admin pages discovery',
            'Basic XSS reflection testing'
        ],
        'usage': [
            'I-type ang website URL (example: google.com)',
            'Click ang "Scan" button',
            'Antayin ang results sa Taglish explanation',
            'Follow ang mga recommended actions'
        ]
    }
    return jsonify(help_info)

if __name__ == '__main__':
    print("🔒 Starting CyberMoriarty Lite Web Interface...")
    app.run(host='0.0.0.0', port=5000, debug=True)