import subprocess
import shlex
import re
import inspect
import json
import requests
import time

class NetworkScan:

    exploits = {}


    def __init__(self):
        self.module = "NMAP"

    def Initial_Scan(self, scan_obj, directory):
        scan_name = inspect.currentframe().f_code.co_name
        scan_obj.db_handler.initialize_function(scan_name, scan_obj.scan_type, self.module)
        output = []
        target = scan_obj.domain if scan_obj.domain else scan_obj.ip
        command = f"nmap -O -sSV -vv -Pn {target} -oN {directory}/{target}-initial -oX {directory}/{target}-initial.xml"
        nmap_proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            for line in iter(nmap_proc.stdout.readline, ''):
                output.append(line.strip() + "\n")
                yield line.strip()

            nmap_proc.wait()

            if nmap_proc.returncode != 0:
                for line in iter(nmap_proc.stderr.readline, ''):
                    yield f"Error: {line.strip()}"
        except Exception as e:
            yield f"Exception: {e}"

        raw_output = ''.join(output)
        scan_obj.db_handler.store_scan_result(scan_name, raw_output)

    def run_intense_scan(self, scan_obj, port, directory):
        scan_name = f"Port {port}"
        scan_obj.db_handler.initialize_function(scan_name, scan_obj.scan_type, self.module, scan_subtype="Analysis")
        scan_obj.db_handler.initialize_function(scan_name, scan_obj.scan_type, self.module, scan_subtype="Intense Scan")
        output = []
        target = scan_obj.domain if scan_obj.domain else scan_obj.ip
        command = f"nmap -sV -Pn -vv -p {port} --script-timeout 90 --script {self.get_nse_script(port)} {target} -oN {directory}/{target}-{port} -oX {directory}/{target}-{port}.xml"
        nmap_proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            for line in iter(nmap_proc.stdout.readline, ''):
                output.append(line.strip() + "\n")
                yield line.strip()

            nmap_proc.wait()

            if nmap_proc.returncode != 0:
                for line in iter(nmap_proc.stderr.readline, ''):
                    yield f"Error: {line.strip()}"
        except Exception as e:
            yield f"Exception: {e}"

        raw_output = ''.join(output)
        scan_obj.db_handler.store_scan_result(scan_name, raw_output, scan_subtype="Intense Scan")
        analysis, _ = self.deep_analysis_parser(raw_output, scan_obj)
        scan_obj.db_handler.store_scan_result(scan_name, analysis, scan_subtype="Analysis")

    def run_nmap_vulnersScan(self, scan_obj, port, directory):
        scan_name = f"Port {port}"
        scan_obj.db_handler.initialize_function(scan_name, scan_obj.scan_type, self.module, scan_subtype="Vulnerability Scan")
        output = []
        target = scan_obj.domain if scan_obj.domain else scan_obj.ip
        command = f"nmap -sV -p {port} --script-timeout 90 --script vulners {target} -oN {directory}/{target}-vulners -oX {directory}/{target}-vulners.xml"
        nmap_proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            for line in iter(nmap_proc.stdout.readline, ''):
                output.append(line.strip() + "\n")
                yield line.strip()

            nmap_proc.wait()

            if nmap_proc.returncode != 0:
                for line in iter(nmap_proc.stderr.readline, ''):
                    yield f"Error: {line.strip()}"
        except Exception as e:
            yield f"Exception: {e}"

        raw_output = ''.join(output)
        scan_obj.db_handler.store_scan_result(scan_name, raw_output, scan_subtype="Vulnerability Scan")

        analysis,exploits_list = self.deep_analysis_parser(raw_output, scan_obj)
        NetworkScan.exploits[port] = exploits_list
        scan_obj.db_handler.store_scan_result(scan_name, analysis, scan_subtype="Analysis")
        
        return exploits_list

    def get_nse_script(self, port):
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
        return nse_scripts.get(str(port), "default")



    def get_cve_details(self, cve_id, delay=1):
        """
        Retrieve CVE details from the NVD API with a time delay between requests.

        :param cve_id: The CVE ID (e.g., "CVE-2021-12345").
        :param delay: The time delay (in seconds) between requests to the API. Default is 1 second.
        :return: A dictionary with CVE details or an error message.
        """
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
        headers = {"User-Agent": "PentekScanner/1.0"}

        try:
            time.sleep(delay)  # Add time delay before making the API request
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                cve = data.get("vulnerabilities", [{}])[0].get("cve", {})
                desc = cve.get("descriptions", [{}])[0].get("value", "No description available.")
                metrics = cve.get("metrics", {})

                cvss_data = None
                if "cvssMetricV31" in metrics:
                    cvss_data = metrics["cvssMetricV31"][0]["cvssData"]
                elif "cvssMetricV30" in metrics:
                    cvss_data = metrics["cvssMetricV30"][0]["cvssData"]
                elif "cvssMetricV2" in metrics:
                    cvss_data = metrics["cvssMetricV2"][0]["cvssData"]

                if cvss_data:
                    score = cvss_data.get("baseScore", "N/A")
                    severity = cvss_data.get("baseSeverity", "N/A")
                else:
                    score = "N/A"
                    severity = "N/A"

                return {
                    "description": desc,
                    "cvss_score": score,
                    "severity": severity
                }
            else:
                return {"error": f"API error {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    # The deep_analysis_parser function already calls get_cve_details when needed
    def deep_analysis_parser(self, raw_output, scan_obj, include_cve=True, include_exploits=True):
        if scan_obj.mode =="cli":
            print("[*] Fetching and Analyzing the Data")
            print("[*] Might Take Time!")
        ip = scan_obj.domain or scan_obj.ip
        summary = [f"[+] Analysis for {ip}"]
        exploit_db_refs = {}
        packet_storm_refs = {}

        # Parse open ports
        port_pattern = re.compile(r"(\d+)/tcp\s+open\s+(\S+)\s+(.*?)\n")
        ports = [f"  - Port {m[0]}/tcp: {m[1]} ({m[2].strip()})" for m in port_pattern.findall(raw_output)]
        if ports:
            summary.append("Open Ports:")
            summary.extend(ports)

        # Include CVEs
        if include_cve:
            cve_pattern = re.compile(r"CVE-\d{4}-\d{4,7}")
            cves = list(set(cve_pattern.findall(raw_output)))
            
            cve_count = 0  # Initialize CVE request count
            if cves:
                summary.append("\nVulnerabilities (CVEs):")
                for cve in cves:
                    if cve_count == 5:  # Check if 5 requests have been made
                        time.sleep(30)  # Delay for 30 seconds
                        cve_count = 0  # Reset request count after delay

                    cve_details = self.get_cve_details(cve, delay=1)  # Add delay here
                    summary.append(f"  - {cve}: {cve_details.get('description', 'No details available')}")
                    # If you want to print the CVSS score and severity as well
                    summary.append(f"    CVSS Score: {cve_details.get('cvss_score', 'N/A')}")
                    summary.append(f"    Severity: {cve_details.get('severity', 'N/A')}")
                    cve_count += 1  # Increment CVE request count

        # Include Exploits
        if include_exploits:
            edb_pattern = re.compile(r"EDB-ID[:\s]+(\d+)")
            edb_ids = list(set(edb_pattern.findall(raw_output)))
            if edb_ids:
                summary.append("\nExploitDB References:")
                for edb in edb_ids:
                    summary.append(f"  - EDB-ID: {edb}")
                    exploit_db_refs[f"EDB-ID:{edb}"] = edb

            packetstorm_pattern = re.compile(r"packetstormsecurity\.com.*?/(\d{4,})")
            ps_ids = list(set(packetstorm_pattern.findall(raw_output)))
            if ps_ids:
                summary.append("\nPacketStorm References:")
                for ps in ps_ids:
                    summary.append(f"  - PacketStorm ID: {ps}")
                    packet_storm_refs[f"PacketStorm-ID:{ps}"] = ps

        # Notes (always include)
        notes = []
        if "vsftpd 2.3.4" in raw_output:
            notes.append("vsftpd 2.3.4 has a known backdoor vulnerability.")
        if re.search(r"Samba smbd 3\.0\.2[0-5]", raw_output):
            notes.append("Samba 3.0.20 through 3.0.25rc3 may allow remote command execution.")
        if "distccd" in raw_output:
            notes.append("Distccd service may allow remote command execution.")
        if notes:
            summary.append("\nNotes:")
            for note in notes:
                summary.append(f"  - {note}")

        exploit_dict = {**exploit_db_refs, **packet_storm_refs}
        return "\n".join(summary), exploit_dict

    @staticmethod
    def run_network_scan(scan_obj, directory):
        obj = NetworkScan()
        open_ports = []
        port_pattern = re.compile(r"(\d+)/tcp\s+(open|filtered|open\\|filtered)")
        try:
            for result in obj.Initial_Scan(scan_obj, directory):
                match = port_pattern.search(result)
                if match:
                    open_ports.append(int(match.group(1)))
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
        print(NetworkScan.exploits)
    

    @staticmethod
    def get_exploits():
        return NetworkScan.exploits

    def ftp_scan(self, scan_obj, directory):
        for result in self.run_intense_scan(scan_obj, 21, directory):
            if scan_obj.mode == "cli":
                print(result)
        for result in self.run_nmap_vulnersScan(scan_obj, 21, directory):
            if scan_obj.mode == "cli":
                print(result)

    def ssh_scan(self, scan_obj, directory):
        for result in self.run_intense_scan(scan_obj, 22, directory):
            if scan_obj.mode == "cli":
                print(result)
        for result in self.run_nmap_vulnersScan(scan_obj, 22, directory):
            if scan_obj.mode == "cli":
                print(result)

    def run_telnet_scanning(self, scan_obj, directory):
        for result in self.run_intense_scan(scan_obj, 23, directory):
            if scan_obj.mode == "cli":
                print(result)
        for result in self.run_nmap_vulnersScan(scan_obj, 23, directory):
            if scan_obj.mode == "cli":
                print(result)

    def run_smtp_scanning(self, scan_obj, directory):
        for result in self.run_intense_scan(scan_obj, 25, directory):
            if scan_obj.mode == "cli":
                print(result)
        for result in self.run_nmap_vulnersScan(scan_obj, 25, directory):
            if scan_obj.mode == "cli":
                print(result)

    def run_dns_scanning(self, scan_obj, directory):
        for result in self.run_intense_scan(scan_obj, 53, directory):
            if scan_obj.mode == "cli":
                print(result)
        for result in self.run_nmap_vulnersScan(scan_obj, 53, directory):
            if scan_obj.mode == "cli":
                print(result)

    def run_rdp_scanning(self, scan_obj, directory):
        for result in self.run_intense_scan(scan_obj, 3389, directory):
            if scan_obj.mode == "cli":
                print(result)
        for result in self.run_nmap_vulnersScan(scan_obj, 3389, directory):
            if scan_obj.mode == "cli":
                print(result)
