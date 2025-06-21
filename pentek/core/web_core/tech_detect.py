# pentek/core/web_core/tech_detect.py

import subprocess

class TechDetect:
    """
    Technology stack detection using WhatWeb and Wappalyzer.
    """
    def __init__(self, db_handler, mode="web"):
        self.module = "TechDetect"
        self.db_handler = db_handler
        self.mode = mode

    def detect_with_whatweb(self, target: str) -> str:
        self.db_handler.initialize_function(target, "WebScan", self.module, scan_subtype="WhatWeb")
        try:
            output = subprocess.getoutput(f"whatweb --no-errors {target}")
        except Exception as e:
            output = f"[!] WhatWeb error: {e}"
        print(output)
        self.db_handler.store_scan_result(target, output, scan_subtype="WhatWeb")

    def detect_with_wappalyzer(self, target: str) -> str:
        self.db_handler.initialize_function(target, "WebScan", self.module, scan_subtype="Wappalyzer")
        try:
            output = subprocess.getoutput(f"wappalyzer {target}")
        except Exception as e:
            output = f"[!] Wappalyzer error: {e}"
        self.db_handler.store_scan_result(target, output, scan_subtype="Wappalyzer")
        print(output)

    @staticmethod
    def run_all(target: str, db_handler, mode: str = "web"):
        """
        One‑line: run WhatWeb then Wappalyzer.
        """
        td = TechDetect(db_handler, mode)
        td.detect_with_whatweb(target)
        td.detect_with_wappalyzer(target)
