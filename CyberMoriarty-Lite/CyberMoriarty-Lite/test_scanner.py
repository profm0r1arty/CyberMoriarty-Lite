#!/usr/bin/env python3
"""
Test script to demonstrate CyberMoriarty Lite functionality
"""

from core.recon import recon
from core.scanner import check_security_headers, find_admin_pages, quick_xss_reflection_test
from assistant import detect_intent, explain_recon, explain_scan_results

def test_scan(url):
    print(f"\n🔎 Testing CyberMoriarty Lite with: {url}")
    print("=" * 60)
    
    try:
        # Run reconnaissance
        print("📍 Running reconnaissance...")
        r = recon(url)
        
        # Run security checks
        print("🛡️ Checking security headers...")
        missing = check_security_headers(url)
        
        print("🔍 Looking for admin pages...")
        admins = find_admin_pages(url)
        
        print("⚠️ Testing for XSS...")
        xss = quick_xss_reflection_test(url)

        # Generate explanations
        print("\n" + "=" * 60)
        print("📊 SCAN RESULTS")
        print("=" * 60)
        
        recon_text = explain_recon(r)
        scan_text = explain_scan_results(missing, admins, xss)

        print("\n🔍 RECONNAISSANCE:")
        print(recon_text)
        
        print("\n🛡️ SECURITY ANALYSIS:")
        print(scan_text)
        
        print("\n" + "=" * 60)
        print("✅ Scan completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during scan: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    # Test with multiple targets
    test_urls = ['google.com', 'example.com']
    
    print("🔒 CyberMoriarty Lite - Test Mode")
    print("Testing cybersecurity scanning capabilities...")
    
    for url in test_urls:
        test_scan(url)
        print("\n" + "="*60 + "\n")