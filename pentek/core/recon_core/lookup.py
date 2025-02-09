import requests
import sys
import subprocess


def whois(domain) -> str:
    '''
        This function look for basic whois information details 
    '''

    whois_cmd  = subprocess.run(f'nslookup {domain}',capture_output=True, text=True, check=True,shell=True)
    print(whois_cmd.stdout)

def lookup_info(domain) -> str:
    '''
        This function look for basic information details like domain name, registry date using whois,dnslookup and other tool
    '''
    nslookup = subprocess.run(f'nslookup {domain}',capture_output=True, text=True, check=True,shell=True)
    print(nslookup.stdout)