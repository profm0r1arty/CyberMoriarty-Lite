from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from core.recon import recon
from core.scanner import check_security_headers, find_admin_pages, quick_xss_reflection_test
from assistant import detect_intent, explain_recon, explain_scan_results

import threading

# Kivy language for layout (keeps design simple, mobile friendly)
kv = '''
<ScannerLayout>:
    orientation: 'vertical'
    padding: dp(12)
    spacing: dp(10)

    TextInput:
        id: url_input
        hint_text: 'Ilagay ang website (e.g. example.com)'
        size_hint_y: None
        height: dp(48)

    Button:
        text: 'Scan (Sari-Sari Mode)'
        size_hint_y: None
        height: dp(48)
        on_press: app.run_full_check()

    ScrollView:
        do_scroll_x: False
        do_scroll_y: True
        GridLayout:
            id: output_grid
            cols: 1
            size_hint_y: None
            height: self.minimum_height

    Button:
        text: 'Switch to Pro Mode'
        size_hint_y: None
        height: dp(40)
        on_press: app.switch_mode()
'''

class ScannerLayout(BoxLayout):
    pass

class CyberMoriartyApp(App):
    def build(self):
        self.mode = 'sari-sari'  # or 'pro'
        Builder.load_string(kv)
        return ScannerLayout()

    def switch_mode(self):
        self.mode = 'pro' if self.mode == 'sari-sari' else 'sari-sari'
        print('Mode switched to', self.mode)

    def run_full_check(self):
        # get URL from TextInput widget
        if self.root and hasattr(self.root, 'ids') and hasattr(self.root.ids, 'url_input'):
            url = self.root.ids.url_input.text.strip()
        else:
            self.show_output('❗ UI not ready')
            return
            
        if not url:
            self.show_output('❗ Please enter website/domain')
            return

        # run in background thread to avoid freezing UI
        t = threading.Thread(target=self._background_check, args=(url,))
        t.daemon = True  # Allow app to exit even if thread is running
        t.start()

    def _background_check(self, url):
        self.show_output('🔎 Nagsi-scan na si Moriarty...')
        
        # Run reconnaissance
        r = recon(url)
        
        # Run security checks
        missing = check_security_headers(url)
        admins = find_admin_pages(url)
        xss = quick_xss_reflection_test(url)

        # Generate explanations
        recon_text = explain_recon(r)
        scan_text = explain_scan_results(missing, admins, xss)

        final = recon_text + '\n\n' + scan_text
        self.show_output(final)

    @mainthread
    def show_output(self, text):
        if self.root and hasattr(self.root, 'ids') and hasattr(self.root.ids, 'output_grid'):
            grid = self.root.ids.output_grid
            grid.clear_widgets()
            
            lbl = Label(
                text=text, 
                size_hint_y=None, 
                text_size=(None, None),
                halign='left',
                valign='top'
            )
            # Set initial height based on text content
            lbl.height = dp(200)
            
            grid.add_widget(lbl)
        else:
            print(f"Output: {text}")

if __name__ == '__main__':
    CyberMoriartyApp().run()
