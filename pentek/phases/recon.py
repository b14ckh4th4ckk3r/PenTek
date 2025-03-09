import sys
import os
import socket
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.recon_core import lookup
from core.recon_core import dns,osint
from addons import delimeter

class Recon:
    def __init__(self,domain,ip):
        self.domain = domain
        self.ip = ip
        self.scan_type = "recon"

    def lookup_info(self,db_handler,mode):
        output = []
        db_handler.initialize_function(self.lookup_info.__name__,self.scan_type)
        db_handler.update_function_status(self.lookup_info.__name__,"running")
        result = lookup.whois(self.domain)
        output.append(result)
        if mode == "cli":
            print(result)
            delimeter.delimeter()

        result = lookup.ns_lookup_info(self.domain)
        output.append("Extracting Information from NS-Lookup\n")
        if mode == "cli":
            print("Extracting Information from NS-Lookup")
            delimeter.delimeter()
            print(result)
            delimeter.delimeter()
        output.append(result)
        output = "".join(output)
        db_handler.store_scan_result(self.lookup_info.__name__,output)

    def dns_info(self,db_handler,mode):
        db_handler.initialize_function(self.dns_info.__name__,self.scan_type)
        db_handler.update_function_status(self.dns_info.__name__,"running")
        output =[]
        temp_result = []
        for line in dns.dnsenumeration(self.domain):
            if mode == "cli":
                print(line)
            temp_result.append(line)
        result = "".join(temp_result)
        output.append(result)
        if mode == "cli":
            delimeter.delimeter()
        # output.append("Searching for Subdomains\n")
        # result = dns.subdomain(self.domain)
        # if mode == "cli":
        #     print(result)
        #     delimeter.delimeter()
        # output.append(result)
        # output = "".join(output)
        db_handler.store_scan_result(self.dns_info.__name__,output)



    @staticmethod
    def recon_run(domain,db_handler,mode):
        ip = socket.gethostbyname(domain)
        recon = Recon(domain,ip)
        scan_type = "recon"
        recon.lookup_info(db_handler,mode)
        recon.dns_info(db_handler,mode)


if __name__ == '__main__':
    domain = input("Enter domain address")
    Recon.recon_run(domain)