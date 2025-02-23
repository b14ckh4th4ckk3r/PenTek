import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.recon_core import lookup
from core.recon_core import dns,osint
from addons import delimeter
def recon_run(domain):
    for output in lookup.whois(domain):
        print(output)

    delimeter.delimeter()
    print("Extracting Information from NS-Lookup")
    delimeter.delimeter()
    for output in lookup.lookup_info(domain):
        print(output)

    delimeter.delimeter()

    # for line in dns.dnsenumeration(domain):
    #     print(line)

    delimeter.delimeter()

    dns.subdomain(domain)




if __name__ == '__main__':
    domain = input("Enter domain address")
    recon_run(domain)