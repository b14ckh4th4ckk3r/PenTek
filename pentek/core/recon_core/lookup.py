import requests
import sys
import subprocess
import shlex
import inspect
from addons.delimeter import delimeter
from colorama import Fore,Back,Style


class LookUp:
    
    def __init__(self):
        self.module = "LookUp"

    def whois(self,recon_obj):
        '''
            This function look for basic whois information details 
        '''
        recon_obj.db_handler.initialize_function(inspect.currentframe().f_code.co_name,recon_obj.scan_type,self.module)
        target = recon_obj.domain
        if not target:
            target = recon_obj.ip
        whois  = subprocess.run(shlex.split(f'whois -H {target}'),capture_output=True, text=True, check=True)
        if recon_obj.mode == "cli":
            print(f"{Fore.GREEN}Extracting Information from Whois{Style.RESET_ALL}")
            print(whois.stdout)
            delimeter()
        recon_obj.db_handler.store_scan_result(inspect.currentframe().f_code.co_name,whois.stdout)

    def ns_lookup(self,recon_obj):
        '''
            This function look for basic information details like domain name, registry date using whois,dnslookup and other tool
        '''
        if recon_obj.domain == '':
            return
        recon_obj.db_handler.initialize_function(inspect.currentframe().f_code.co_name,recon_obj.scan_type,self.module)
        nslookup = subprocess.run(shlex.split(f'nslookup {recon_obj.domain}'),capture_output=True, text=True, check=True)
        if recon_obj.mode == "cli":
            print(f"{Fore.GREEN}Extracting Information from NS-Lookup\n{Style.RESET_ALL}")
            print(nslookup.stdout)
            delimeter()
        recon_obj.db_handler.store_scan_result(inspect.currentframe().f_code.co_name,nslookup.stdout)
    
    @staticmethod
    def run_lookup(recon_obj):
        obj = LookUp()
        obj.whois(recon_obj)
        obj.ns_lookup(recon_obj)

    
        