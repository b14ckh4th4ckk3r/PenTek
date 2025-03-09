import os
from pathlib import Path
import socket
import re
from datetime import datetime


from core.scanning_core import network
from addons import delimeter
from database.mongodb_handler import MongoDBHandler


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
                print(result,flush=True)
            
    
    except Exception as e:
        print(e)
    
    delimeter.delimeter()

    for port in open_ports:
        scan_function = {
            21: network.run_ftp_scanning,
            22: network.run_ssh_scanning,
            23: network.run_telnet_scanning,
            25: network.run_smtp_scanning,
            53: network.run_dns_scanning,
            3389: network.run_rdp_scanning
        }.get(port, None)

        if scan_function:
            for result in scan_function(ip, directory, mode):
                if mode == "cli":
                    print(result)
                else:
                    # yield result
                    pass
                
            if mode == "cli":
                delimeter.delimeter()




def run_scanning(domain,mode):
    try:

        home_dir = Path.home()
        os.makedirs(home_dir / domain,exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        directory = home_dir / domain / f'nmap_result_for_{domain}_{timestamp}/'
        os.makedirs(directory,exist_ok=True)

    except Exception as e:
        print(f'Error: {e}')
    ip = socket.gethostbyname(domain)
    network_scanning(ip, mode, directory)

if __name__ == "__main__":
    # domain = input("Enter the domain for Scanning: ")
    domain = "192.168.10.4"
    

    run_scanning(domain,"cli")
    