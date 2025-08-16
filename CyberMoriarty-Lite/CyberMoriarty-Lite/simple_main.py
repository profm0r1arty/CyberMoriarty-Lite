#!/usr/bin/env python3
"""
CyberMoriarty Lite - Simple Console Version
A command-line cybersecurity reconnaissance tool with Taglish assistant interface
"""

from core.recon import recon
from core.scanner import check_security_headers, find_admin_pages, quick_xss_reflection_test
from assistant import detect_intent, explain_recon, explain_scan_results

def main():
    print("🔒 CyberMoriarty Lite - Cybersecurity Scanner")
    print("=" * 50)
    print("Mga commands:")
    print("- 'scan [website]' - I-scan ang website")
    print("- 'help' - Tingnan ang mga commands")
    print("- 'exit' - Umalis sa program")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\nCyberMoriarty> ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit', 'stop']:
                print("Salamat sa paggamit ng CyberMoriarty Lite!")
                break
                
            if user_input.lower() in ['help', 'tulong']:
                show_help()
                continue
            
            # Check if it's a scan command
            if user_input.lower().startswith(('scan ', 'check ', 'tingnan ')):
                # Extract URL from command
                parts = user_input.split(' ', 1)
                if len(parts) > 1:
                    url = parts[1].strip()
                    run_scan(url)
                else:
                    print("❗ Kulang ang URL. Example: scan google.com")
            else:
                # Try to detect if it's just a URL
                if '.' in user_input and not user_input.startswith('http'):
                    run_scan(user_input)
                else:
                    print("❓ Hindi ko maintindihan. Type 'help' para sa mga commands.")
                    
        except KeyboardInterrupt:
            print("\nSalamat sa paggamit ng CyberMoriarty Lite!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def show_help():
    print("""
🔍 CyberMoriarty Lite Help

Mga available commands:
- scan [website] - Mag-scan ng website
- help / tulong - Show this help
- exit / quit - Close ang program

Mga examples:
- scan google.com
- scan https://example.com
- tingnan facebook.com

Mga features:
✓ DNS resolution at IP lookup
✓ HTTPS/SSL status check
✓ Security headers analysis
✓ Admin pages discovery
✓ Basic XSS reflection test

Lahat ng results ay nasa Taglish para mas madaling maintindihan!
    """)

def run_scan(url):
    print(f"\n🔎 Nagsi-scan si Moriarty ng: {url}")
    print("-" * 40)
    
    try:
        # Run reconnaissance
        print("📍 Gathering basic info...")
        r = recon(url)
        
        # Run security checks
        print("🛡️ Checking security headers...")
        missing = check_security_headers(url)
        
        print("🔍 Looking for admin pages...")
        admins = find_admin_pages(url)
        
        print("⚠️ Testing for XSS...")
        xss = quick_xss_reflection_test(url)

        # Generate explanations
        print("\n" + "=" * 50)
        print("📊 SCAN RESULTS")
        print("=" * 50)
        
        recon_text = explain_recon(r)
        scan_text = explain_scan_results(missing, admins, xss)

        print("\n🔍 RECONNAISSANCE:")
        print(recon_text)
        
        print("\n🛡️ SECURITY ANALYSIS:")
        print(scan_text)
        
        print("\n" + "=" * 50)
        
    except Exception as e:
        print(f"❌ Error during scan: {e}")

if __name__ == '__main__':
    main()