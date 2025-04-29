import requests
import sys
import subprocess
import shlex


class LookUp:
    def __init__(self,domain):
        self.domain = domain
        
    def whois(self):
        '''
            This function look for basic whois information details 
        '''

        whois  = subprocess.run(shlex.split(f'whois -H {self.domain}'),capture_output=True, text=True, check=True)
        return whois.stdout

    def ns_lookup_info(self):
        '''
            This function look for basic information details like domain name, registry date using whois,dnslookup and other tool
        '''
        nslookup = subprocess.run(shlex.split(f'nslookup {self.domain}'),capture_output=True, text=True, check=True)
        return nslookup.stdout
    
        