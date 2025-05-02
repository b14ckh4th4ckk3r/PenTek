import os
from pathlib import Path
import socket
import re
import ipaddress
from datetime import datetime
from core.scanning_core.network import NetworkScan
from addons import delimeter
from database.mongodb_handler import MongoDBHandler

class Scanning:
    def __init__(self,domain,ip,db_handler,mode="web"):
        self.domain = domain
        self.ip = ip
        self.scan_type = "Scanning"
        self.db_handler = db_handler
        self.mode = mode

    def network_scanning(self,directory):
        NetworkScan.run_network_scan(self,directory)
        
        



    @staticmethod
    def run_scanning(domain,db_handler,mode):
        try:

            home_dir = Path.home()
            os.makedirs(home_dir / domain,exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            directory = home_dir / domain / f'nmap_result_for_{domain}_{timestamp}/'
            os.makedirs(directory,exist_ok=True)
            ip = ""
            try:
                ipaddress.ip_address(domain)
                ip = domain
                domain = ''

            except:
                ip = socket.gethostbyname(domain)
            finally:
                scan_obj = Scanning(domain,ip,db_handler,mode)
                scan_obj.network_scanning(directory)

        except Exception as e:
            print(f'Error: {e}')

if __name__ == "__main__":
    # domain = input("Enter the domain for Scanning: ")
    domain = "192.168.10.4"
    Scanning.run_scanning(domain,"cli")
    