import subprocess
import shlex
import inspect
from addons import delimeter
from colorama import Fore,Back,Style

class OSINT:

    def __init__(self):
        self.module = "OSINT"

    def theHarvester(self,recon_obj):
        '''
            This function runs theHarvester to gather emails, hosts, and other intel using public sources.
        '''
    

        recon_obj.db_handler.initialize_function(inspect.currentframe().f_code.co_name,recon_obj.scan_type,self.module)
        if recon_obj.mode == "cli":
            print(f"{Fore.RED}[*] ===== Running TheHarvestor ====={Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] ===== Might Take Some Time ====={Style.RESET_ALL}")
        command = f'theHarvester -d {recon_obj.domain} -b anubis,baidu,bing,brave,crtsh,dnsdumpster,duckduckgo,hackertarget,otx,rapiddns,sitedossier,subdomaincenter,subdomainfinderc99,threatminer,urlscan,yahoo -l 100'
        result = subprocess.run(shlex.split(command),text=True,capture_output=True)
     
        if recon_obj.mode == "cli":
            print(result.stdout)
        recon_obj.db_handler.store_scan_result(inspect.currentframe().f_code.co_name,result.stdout)

    def whatweb(self,recon_obj):
        '''
            This function uses WhatWeb to fingerprint web technologies from a domain or IP.
        '''
        recon_obj.db_handler.initialize_function(inspect.currentframe().f_code.co_name,recon_obj.scan_type,self.module)
        command = f'whatweb {recon_obj.domain}'
        result = subprocess.run(shlex.split(command), capture_output=True, text=True, check=True)
        if recon_obj.mode == "cli":
            print(result.stdout)
        recon_obj.db_handler.store_scan_result(inspect.currentframe().f_code.co_name,result.stdout)

    def holehe(self,email,recon_obj):
        '''
            This function runs Holehe to check if an email is used on different websites.
        '''
        recon_obj.db_handler.initialize_function(inspect.currentframe().f_code.co_name,recon_obj.scan_type,self.module)
        command = f'holehe {email}'
        result = subprocess.run(shlex.split(command), capture_output=True, text=True, check=True)
        if recon_obj.mode == "cli":
            print(result.stdout)
        recon_obj.db_handler.store_scan_result(inspect.currentframe().f_code.co_name,result.stdout)

    def sherlock(self,username,recon_obj):
        '''
            This function runs Sherlock to check for a username across social networks.
        '''
        recon_obj.db_handler.initialize_function(inspect.currentframe().f_code.co_name,recon_obj.scan_type,self.module)
        command = f'python3 sherlock/sherlock.py {username}'
        result = subprocess.run(shlex.split(command), capture_output=True, text=True, check=True)
        if recon_obj.mode == "cli":
            print(result.stdout)
        recon_obj.db_handler.store_scan_result(inspect.currentframe().f_code.co_name,result.stdout)

    def ghunt(self,email,recon_obj):
        '''
            This function runs GHunt for Google account-related OSINT using an email address.
        '''
        recon_obj.db_handler.initialize_function(inspect.currentframe().f_code.co_name,recon_obj.scan_type,self.module)
        command = f'python3 GHunt/ghunt.py email {email}'
        result = subprocess.run(shlex.split(command), capture_output=True, text=True, check=True)
        if recon_obj.mode == "cli":
            print(result.stdout)
        recon_obj.db_handler.store_scan_result(inspect.currentframe().f_code.co_name,result.stdout)
    

    @staticmethod
    def run_osint(recon_obj):
        obj = OSINT()
        obj.theHarvester(recon_obj)
        obj.whatweb(recon_obj)


