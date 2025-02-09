import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core import recon_core
from addons import delimeter
def run(ip):
    recon_core.whois(ip)

    delimeter.delimeter()
    recon_core.lookup_info(ip)

    delimeter.delimeter()

    recon_core.dnsenumeration(ip)




if __name__ == '__main__':
    ip = input("Enter IP address")
    run(ip)