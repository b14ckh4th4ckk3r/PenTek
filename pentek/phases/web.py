# pentek/core/phases/web.py

import socket
import ipaddress

from core.web_core.tech_detect import TechDetect
from core.web_core.dir_enum       import DirEnum
from core.web_core.vuln_scan      import VulnScan
from core.web_core.param_enum     import ParamEnum
from core.web_core.web_exploits   import WebExploits

class WebExploitation:
    """
    Mirrors your network Exploitation class: static entry point + instance method.
    Discovers endpoints via fuzzing, enumerates params, scans, then exploits.
    """
    def __init__(self, domain, ip, db_handler, mode="cli"):
        self.domain     = domain
        self.ip         = ip
        self.scan_type  = "Web"
        self.db_handler = db_handler
        self.mode       = mode

    def run_web_exploit(self,
                        params_map,
                        wordlist="/usr/share/seclists/Discovery/Web-Content/common.txt",
                        param_wordlist="/usr/share/seclists/Discovery/Web-Content/raft-small-params.txt",
                        nuclei_templates="cves/"):
        target = f'http://{self.domain or self.ip}'

        # 1. Tech detection
        TechDetect.run_all(target, self.db_handler, self.mode)

        # 2. Directory enumeration
        dir_out = DirEnum.run_all(target, self.db_handler, self.mode, wordlist=wordlist) or ""
        paths = [line.split()[1] for line in dir_out.splitlines() if line.startswith("/")]

        # 3. Parameter enumeration (fuzz discovered paths)
        params_map = ParamEnum.run_all(target, self.db_handler, self.mode,
                                       dir_paths=paths,
                                       param_wordlist=param_wordlist)
        print("Param")
        print(params_map)
        # 4. Vulnerability scanning
        VulnScan.run_all(target, self.db_handler, self.mode, templates=nuclei_templates)

        # 5. Exploitation on discovered params
        if params_map:
            # build exp_obj for WebExploits
            exp_obj = type("EObj", (), {
                "ip":         self.ip,
                "domain":     self.domain,
                "scan_type":  self.scan_type,
                "db_handler": self.db_handler,
                "mode":       self.mode
            })()
            for ep, params in params_map.items():
                full = target.rstrip("/") + ep
                WebExploits.run_all(exp_obj, full, params)

    @staticmethod
    def run_all(domain, db_handler, mode="cli",
                        wordlist="/usr/share/seclists/Discovery/Web-Content/common.txt",
                        param_wordlist="/usr/share/seclists/Discovery/Web-Content/raft-small-params.txt",
                        nuclei_templates="cves/"):
        """
        Static entry point—resolve domain/IP, instantiate, then run.
        """
        try:
            # if domain is actually an IP address
            ipaddress.ip_address(domain)
            ip     = domain
            domain = ""
        except ValueError:
            ip = socket.gethostbyname(domain)

        web = WebExploitation(domain, ip, db_handler, mode)
        web.run_web_exploit(params_map=None,
                            wordlist=wordlist,
                            param_wordlist=param_wordlist,
                            nuclei_templates=nuclei_templates)
