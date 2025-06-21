# pentek/core/web_core/vuln_scan.py

import subprocess

class VulnScan:
    """
    Vulnerability scanning using Nikto and Nuclei.
    """
    def __init__(self, db_handler, mode="web"):
        self.module = "VulnScan"
        self.db_handler = db_handler
        self.mode = mode

    def run_nikto(self, target: str) -> str:
        self.db_handler.initialize_function(target, "WebScan", self.module, scan_subtype="Nikto")
        try:
            output = subprocess.getoutput(f"nikto -h {target}")
        except Exception as e:
            output = f"[!] Nikto error: {e}"
        self.db_handler.store_scan_result(target, output, scan_subtype="Nikto")
        print(output)

    def run_nuclei(self, target: str, templates: str = "cves/") -> str:
        self.db_handler.initialize_function(target, "WebScan", self.module, scan_subtype="Nuclei")
        try:
            output = subprocess.getoutput(f"nuclei -u {target} -t {templates}")
        except Exception as e:
            output = f"[!] Nuclei error: {e}"
        self.db_handler.store_scan_result(target, output, scan_subtype="Nuclei")
        print(output)

    @staticmethod
    def run_all(target: str, db_handler, mode: str = "web", templates: str = "cves/"):
        """
        One‑line: run Nikto then Nuclei.
        """
        vs = VulnScan(db_handler, mode)
        vs.run_nikto(target)
        vs.run_nuclei(target, templates)
