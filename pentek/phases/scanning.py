import sys
import os
import socket
import re
import subprocess,shlex
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from core.scanning_core import network
from addons import delimeter
def network_scanning(ip,mode,directory):
    open_ports = []
    port_pattern = re.compile(r"(\d+)/tcp\s+(open|filtered)")
    try:
        for result in network.run_initial_scan(ip,directory):
            match = port_pattern.search(result)
            if match:
                # open_ports.append((match.group(1), match.group(2)))
                open_ports.append(int(match.group(0).split("/")[0]))
            if mode == 'cli':
                print(result)
            else:
                pass
    
    except Exception as e:
        print(e)
    
    delimeter.delimeter()


    if 21 in open_ports:
        network.run_ftp_scanning(domain,directory,mode)


    if 22 in open_ports:
        network.run_ssh_scanning(domain,directory,mode)

    delimeter.delimeter()

    if 23 in open_ports:
        network.run_telnet_scanning(domain,directory,mode)

    delimeter.delimeter()

    if 25 in open_ports:
        network.run_smtp_scanning(domain,directory,mode)

    delimeter.delimeter()

    if 53 in open_ports:
        network.run_dns_scanning(domain,directory,mode)

    delimeter.delimeter()

    if 3389 in open_ports:
        network.run_rdp_scanning(domain,directory,mode)




def run_scanning(domain,mode):
    try:
        path = subprocess.run(f'echo $HOME',capture_output=True,text=True,shell=True)
        pathw =path.stdout[0:-1]

        directory = f'{pathw}/nmap_result_{domain}'
        try:
            subprocess.run(shlex.split(f'mkdir {directory}'),capture_output=True,check=True)

        except Exception as e:
            subprocess.run(shlex.split(f'bash && rm -rf -- {directory}/*'),capture_output=True,check=True)
    except Exception as e:
        pass
    ip = socket.gethostbyname(domain)
    network_scanning(ip,mode,directory)

if __name__ == "__main__":
    # domain = input("Enter the domain for Scanning: ")
    domain = "192.168.10.4"
    

    run_scanning(domain,"cli")
    