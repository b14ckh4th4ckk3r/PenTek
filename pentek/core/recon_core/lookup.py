import requests
import sys
import subprocess
import shlex


def whois(domain):
    '''
        This function look for basic whois information details 
    '''

    whois  = subprocess.run(shlex.split(f'whois -H {domain}'),capture_output=True, text=True, check=True)
    return whois.stdout

def ns_lookup_info(domain):
    '''
        This function look for basic information details like domain name, registry date using whois,dnslookup and other tool
    '''
    nslookup = subprocess.run(shlex.split(f'nslookup {domain}'),capture_output=True, text=True, check=True)
    return nslookup.stdout