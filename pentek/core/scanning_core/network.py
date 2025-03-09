import subprocess
import shlex
import re

def run_initial_scan(target,directory):
    """Run the initial intense Nmap scan to identify open and filtered ports."""
    command = f"nmap -O -sSV -vv -Pn {target} -oN {directory}/{target}-initial -oX {directory}/{target}-initial.xml"
    nmap_proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        for line in iter(nmap_proc.stdout.readline, ''):
            yield line.strip()

        # Wait for the process to finish
        nmap_proc.wait()


        if nmap_proc.returncode != 0:
            for line in iter(nmap_proc.stderr.readline, ''):
                yield f"Error: {line.strip()}"
    except Exception as e:
        yield f"Exception: {e}"

def run_intense_scan(target, port, directory):
    """Run a detailed Nmap NSE scan for a specific open or filtered port."""
    command = f"nmap -sV -Pn -vv -p {port} --script-timeout 90 --script {get_nse_script(port)} {target} -oN {directory}/{target}-{port} -oX {directory}/{target}-{port}.xml"
    nmap_proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        # Stream stdout line by line
        for line in iter(nmap_proc.stdout.readline, ''):
            yield line.strip()

        # Wait for the process to finish
        nmap_proc.wait()

        # Check for errors
        if nmap_proc.returncode != 0:
            for line in iter(nmap_proc.stderr.readline, ''):
                yield f"Error: {line.strip()}"

    except Exception as e:
        yield f"Exception: {e}"

def get_nse_script(port):
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

def run_nmap_vulnersScan(target,port,directory):
    '''Run a vulners script scan on a specified port for '''
    command = f"nmap -sV -p {port} --script-timeout 90 --script vulners {target} -oN {directory}/{target}-vulners -oX {directory}/{target}-vulners.xml"
    nmap_proc = subprocess.Popen(shlex.split(command),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    try:
        for line in iter(nmap_proc.stdout.readline,' '):
            yield line.strip()
        
        nmap_proc.wait()

        # Check for errors
        if nmap_proc.returncode != 0:
            for line in iter(nmap_proc.stderr.readline, ''):
                yield f"Error: {line.strip()}"
    except Exception as e:
        yield f"Exception: {e}"


def run_ftp_scanning(domain,directory,mode):
    '''This Fucntion will scan for FTP vulnerablities'''
    
    print("====== Running detailed nmap scan for port 21 ======")
    for result in run_intense_scan(domain,21,directory):
        if mode == "cli":
            print(result)
        else:
            pass
        
    print("====== Running detailed nmap scan for port 21 ======")
    for result in run_nmap_vulnersScan(domain,21,directory):
        if mode == "cli":
            print(result)
            print()
        else:   
            pass
def run_ssh_scanning(domain,directory,mode):
    '''This Fucntion will scan for ssh vulnerablities'''

    for result in run_intense_scan(domain,22,directory):
        if mode == "cli":
            print("====== Running detailed nmap scan for port 22 ======")
            print(result)
            print()

        else:
            pass


def run_telnet_scanning(domain,directory,mode):
    '''This Fucntion will scan for TELNET vulnerablities'''

    for result in run_intense_scan(domain,23,directory):
        if mode == "cli":
            print("====== Running detailed nmap scan for port 23 ======")
            print(result)
            print()
        else:
            pass

def run_smtp_scanning(domain,directory,mode):
    '''This Fucntion will scan for SMTP vulnerablities'''

    for result in run_intense_scan(domain,25,directory):
        if mode == "cli":
            print("====== Running detailed nmap scan for port 25 ======")
            print(result)
            print()
        else:
            pass

def run_dns_scanning(domain,directory,mode):
    '''This Fucntion will scan for DNS vulnerablities'''

    for result in run_intense_scan(domain,53,directory):
        if mode == "cli":
            print("====== Running detailed nmap scan for port 53 ======")
            print(result)
            print()
        else:
            pass


def run_rdp_scanning(domain,directory,mode):
    '''This Fucntion will scan for RDP vulnerablities'''

    for result in run_intense_scan(domain,3389,directory):
        if mode == "cli":
            print("====== Running detailed nmap scan for port 3389 ======")
            print(result)
            print()
        else:
            pass





if __name__ == "__main__":
    target = "testfire.net"

    print("[+] Initial Nmap scan output:")
    open_ports = []
    for output in run_initial_scan(target):
        print(output)
        if isinstance(output, list):
            open_ports = output

    if open_ports:
        print(f"[+] Found {len(open_ports)} open/filtered ports: {open_ports}")
        for port, state in open_ports:
            print(f"[+] Detailed scan for port {port}:")
            for output in run_intense_scan(target, port):
                print(output)
    else:
        print("[!] No open or filtered ports found.")
