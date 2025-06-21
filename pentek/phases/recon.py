import socket
from core.recon_core.lookup import LookUp
from core.recon_core.dns import DNS
from core.recon_core.osint import OSINT
import ipaddress


class Recon:
    def __init__(self,domain,ip,db_handler,mode="web"):
        self.domain = domain
        self.ip = ip
        self.scan_type = "Recon"
        self.db_handler = db_handler
        self.mode = mode

    def lookup_info(self):
        LookUp.run_lookup(self)

    def dns_info(self):
        DNS.run_dns(self)

    def osint(self):
        OSINT.run_osint(self)
        




    @staticmethod
    def recon_run(domain,db_handler,mode):
        ip = ""
        try:
            ipaddress.ip_address(domain)
            ip = domain
            domain = ''

        except:
            ip = socket.gethostbyname(domain)
        recon = Recon(domain,ip,db_handler,mode)
        recon.lookup_info()
        recon.dns_info()
        recon.osint()


if __name__ == '__main__':
    domain = input("Enter domain address")
    Recon.recon_run(domain)