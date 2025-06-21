# pentek/core/web_core/dir_enum.py

import subprocess

class DirEnum:
    """
    Directory brute‑forcing using ffuf.
    """
    def __init__(self, db_handler, mode="web"):
        self.module = "DirEnum"
        self.db_handler = db_handler
        self.mode = mode

    def run_ffuf(self, target: str, wordlist: str = "common.txt", threads: int = 50) -> str:
        self.db_handler.initialize_function(target, "WebScan", self.module, scan_subtype="FFUF")
        cmd = f"ffuf -u {target}/FUZZ -w {wordlist} -s -t {threads}"
        try:
            output = subprocess.getoutput(cmd)
        except Exception as e:
            output = f"[!] FFUF error: {e}"
        self.db_handler.store_scan_result(target, output, scan_subtype="FFUF")
        print(output)

    @staticmethod
    def run_all(target: str, db_handler, mode: str = "web", wordlist: str = "common.txt", threads: int = 50):
        """
        One‑line: run ffuf with defaults.
        """
        DirEnum(db_handler, mode).run_ffuf(target, wordlist, threads)
