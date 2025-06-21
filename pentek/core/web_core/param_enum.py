# pentek/core/web_core/param_enum.py

import subprocess
import requests
from bs4 import BeautifulSoup
import re

class ParamEnum:
    """
    Crawl and fuzz to discover injectable parameters.
    """
    def __init__(self, db_handler, mode="web"):
        self.module = "ParamEnum"
        self.db_handler = db_handler
        self.mode = mode

    def crawl_endpoints(self, base_url: str, paths: list) -> set:
        discovered = set()
        headers = {"User-Agent": "Mozilla/5.0"}
        for p in paths:
            url = base_url.rstrip("/") + "/" + p.lstrip("/")
            try:
                r = requests.get(url, headers=headers, timeout=5)
                text = r.text
                for match in re.findall(r'href=["\']([^"\']+\?[^"\']+)["\']', text):
                    discovered.add(match)
                soup = BeautifulSoup(text, "html.parser")
                for form in soup.find_all("form"):
                    action = form.get("action") or ""
                    if "?" in action:
                        discovered.add(action)
            except Exception:
                continue
        return discovered

    def fuzz_params(self, target: str, endpoint: str, param_wordlist: str, threads: int = 25) -> list:
        self.db_handler.initialize_function(endpoint, "WebScan", self.module, scan_subtype="ParamFuzz")
        cmd = f"ffuf -u {target.rstrip('/')}/{endpoint.lstrip('/')}?FUZZ=1 -w {param_wordlist} -s -t {threads}"
        try:
            output = subprocess.getoutput(cmd)
        except Exception as e:
            output = f"[!] Param fuzz error: {e}"
        self.db_handler.store_scan_result(endpoint, output, scan_subtype="ParamFuzz")
        params = re.findall(r'\?([^=]+)=', output)
        return list(set(params))

    @staticmethod
    def run_all(target: str, db_handler, mode: str = "web", dir_paths: list = None, param_wordlist: str = "/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt"):
        pe = ParamEnum(db_handler, mode)
        if dir_paths is None:
            from core.web_core.dir_enum import DirEnum
            out = DirEnum(db_handler, mode).run_ffuf(target)
            dir_paths = [line.split()[1] for line in (out or "").splitlines() if "/" in line]
        endpoints = pe.crawl_endpoints(target, dir_paths)
        param_map = {}
        for ep in endpoints:
            params = pe.fuzz_params(target, ep, param_wordlist)
            if params:
                param_map[ep] = params
        return param_map
