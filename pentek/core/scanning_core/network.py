import subprocess
import shlex
import re
import inspect 

class NetworkScan:
    def __init__(self):
        self.module = "NMAP"

    def Initial_Scan(self, scan_obj, directory):
        """Run the initial intense Nmap scan to identify open and filtered ports."""
        scan_obj.db_handler.initialize_function(inspect.currentframe().f_code.co_name, scan_obj.scan_type, self.module)
        output = []
        target = scan_obj.domain if scan_obj.domain else scan_obj.ip
        command = f"nmap -O -sSV -vv -Pn {target} -oN {directory}/{target}-initial -oX {directory}/{target}-initial.xml"
        nmap_proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            for line in iter(nmap_proc.stdout.readline, ''):
                yield line.strip()
                output.append(line.strip() + "\n")

            nmap_proc.wait()

            if nmap_proc.returncode != 0:
                for line in iter(nmap_proc.stderr.readline, ''):
                    yield f"Error: {line.strip()}"
        except Exception as e:
            yield f"Exception: {e}"

        scan_obj.db_handler.store_scan_result(inspect.currentframe().f_code.co_name, ''.join(output))

    def run_intense_scan(self, scan_obj, port, directory):
        """Run a detailed Nmap NSE scan for a specific open or filtered port."""
        scan_name = f'Port {port}'
        scan_obj.db_handler.initialize_function(scan_name, scan_obj.scan_type, self.module, scan_subtype="Intense Scan")
        output = []
        target = scan_obj.domain if scan_obj.domain else scan_obj.ip
        command = f"nmap -sV -Pn -vv -p {port} --script-timeout 90 --script {self.get_nse_script(port)} {target} -oN {directory}/{target}-{port} -oX {directory}/{target}-{port}.xml"
        nmap_proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            for line in iter(nmap_proc.stdout.readline, ''):
                yield line.strip()
                output.append(line.strip() + "\n")

            nmap_proc.wait()

            if nmap_proc.returncode != 0:
                for line in iter(nmap_proc.stderr.readline, ''):
                    yield f"Error: {line.strip()}"

        except Exception as e:
            yield f"Exception: {e}"

        scan_obj.db_handler.store_scan_result(scan_name, ''.join(output), scan_subtype="Intense Scan")

    def get_nse_script(self, port):
        """Return appropriate NSE script based on the port number."""
        nse_scripts = {
            "21": "ftp-*",
            "22": "ssh-*",
            "23": "telnet-*",
            "25": "smtp-*",
            "53": "dns-*",
            "80": "http-*",
            "443": "ssl-*",
            "3389": "rdp-*",
        }
        return nse_scripts.get(port, "default")

    def run_nmap_vulnersScan(self, scan_obj, port, directory):
        '''Run a vulners script scan on a specified port'''
        scan_name = f'Port {port}'
        scan_obj.db_handler.initialize_function(scan_name, scan_obj.scan_type, self.module, scan_subtype="Vulnerability Scan")
        output = []
        target = scan_obj.domain if scan_obj.domain else scan_obj.ip
        command = f"nmap -sV -p {port} --script-timeout 90 --script vulners {target} -oN {directory}/{target}-vulners -oX {directory}/{target}-vulners.xml"
        nmap_proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            for line in iter(nmap_proc.stdout.readline, ''):
                yield line.strip()
                output.append(line.strip() + "\n")

            nmap_proc.wait()

            if nmap_proc.returncode != 0:
                for line in iter(nmap_proc.stderr.readline, ''):
                    yield f"Error: {line.strip()}"

        except Exception as e:
            yield f"Exception: {e}"

        scan_obj.db_handler.store_scan_result(scan_name, ''.join(output), scan_subtype="Vulnerability Scan")

    def ftp_scan(self, scan_obj, directory):
        '''Scan for FTP vulnerabilities'''
        if scan_obj.mode == "cli":
            print("====== Running detailed nmap scan for port 21 ======")
        for result in self.run_intense_scan(scan_obj, 21, directory):
            if scan_obj.mode == "cli":
                print(result)
        print()
        if scan_obj.mode == "cli":
            print("====== Running Vulnerability nmap scan for port 21 ======")
        for result in self.run_nmap_vulnersScan(scan_obj, 21, directory):
            if scan_obj.mode == "cli":
                print(result)
        print()

    def ssh_scan(self, scan_obj, directory):
        '''Scan for SSH vulnerabilities'''
        if scan_obj.mode == "cli":
            print("====== Running detailed nmap scan for port 22 ======")
        for result in self.run_intense_scan(scan_obj, 22, directory):
            if scan_obj.mode == "cli":
                print(result)
        print()
        if scan_obj.mode == "cli":
            print("====== Running Vulnerability nmap scan for port 22 ======")
        for result in self.run_nmap_vulnersScan(scan_obj, 22, directory):
            if scan_obj.mode == "cli":
                print(result)

    def run_telnet_scanning(self, scan_obj, directory):
        '''Scan for TELNET vulnerabilities'''
        if scan_obj.mode == "cli":
            print("====== Running detailed nmap scan for port 23 ======")
        for result in self.run_intense_scan(scan_obj, 23, directory):
            if scan_obj.mode == "cli":
                print(result)
        print()
        if scan_obj.mode == "cli":
            print("====== Running Vulnerability nmap scan for port 23 ======")
        for result in self.run_nmap_vulnersScan(scan_obj, 23, directory):
            if scan_obj.mode == "cli":
                print(result)

    def run_smtp_scanning(self, scan_obj, directory):
        '''Scan for SMTP vulnerabilities'''
        if scan_obj.mode == "cli":
            print("====== Running detailed nmap scan for port 25 ======")
        for result in self.run_intense_scan(scan_obj, 25, directory):
            if scan_obj.mode == "cli":
                print(result)
        print()
        if scan_obj.mode == "cli":
            print("====== Running Vulnerability nmap scan for port 25 ======")
        for result in self.run_nmap_vulnersScan(scan_obj, 25, directory):
            if scan_obj.mode == "cli":
                print(result)

    def run_dns_scanning(self, scan_obj, directory):
        '''Scan for DNS vulnerabilities'''
        if scan_obj.mode == "cli":
            print("====== Running detailed nmap scan for port 53 ======")
        for result in self.run_intense_scan(scan_obj, 53, directory):
            if scan_obj.mode == "cli":
                print(result)
        print()
        if scan_obj.mode == "cli":
            print("====== Running Vulnerability nmap scan for port 53 ======")
        for result in self.run_nmap_vulnersScan(scan_obj, 53, directory):
            if scan_obj.mode == "cli":
                print(result)

    def run_rdp_scanning(self, scan_obj, directory):
        '''Scan for RDP vulnerabilities'''
        if scan_obj.mode == "cli":
            print("====== Running detailed nmap scan for port 3389 ======")
        for result in self.run_intense_scan(scan_obj, 3389, directory):
            if scan_obj.mode == "cli":
                print(result)
        print()
        if scan_obj.mode == "cli":
            print("====== Running Vulnerability nmap scan for port 3389 ======")
        for result in self.run_nmap_vulnersScan(scan_obj, 3389, directory):
            if scan_obj.mode == "cli":
                print(result)

    @staticmethod
    def run_network_scan(scan_obj, directory):
        obj = NetworkScan()
        open_ports = []
        port_pattern = re.compile(r"(\d+)/tcp\s+(open|filtered)")
        try:
            for result in obj.Initial_Scan(scan_obj, directory):
                match = port_pattern.search(result)
                if match:
                    open_ports.append(int(match.group(0).split("/")[0]))
                if scan_obj.mode == 'cli':
                    print(result, flush=True)

        except Exception as e:
            print(e)
        for port in open_ports:
            scan_function = {
                21: obj.ftp_scan,
                22: obj.ssh_scan,
                23: obj.run_telnet_scanning,
                25: obj.run_smtp_scanning,
                53: obj.run_dns_scanning,
                3389: obj.run_rdp_scanning
            }.get(port, None)
            if scan_function:
                scan_function(scan_obj, directory)
