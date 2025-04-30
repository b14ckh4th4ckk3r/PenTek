import subprocess
import shlex
import inspect
from addons.delimeter import delimeter
from colorama import Fore,Back,Style


class DNS:

    def __init__(self):
        self.module = "DNS"

    def dig(self,recon_obj):
        ''' This fucntion perform basic dns enumeration. '''
        recon_obj.db_handler.initialize_function(inspect.currentframe().f_code.co_name,recon_obj.scan_type,self.module)
        dig = subprocess.run(shlex.split(f'dig all +short {recon_obj.domain} q-type * q-class *'),capture_output=True,text=True)
        
        if recon_obj.mode == "cli":
            print(dig.stdout)
            delimeter()
        
        recon_obj.db_handler.store_scan_result(inspect.currentframe().f_code.co_name,dig.stdout)
        
    def dnsenum(self,recon_obj):

        recon_obj.db_handler.initialize_function(inspect.currentframe().f_code.co_name,recon_obj.scan_type,self.module)
        dnsenum = subprocess.Popen(shlex.split(f'dnsenum {recon_obj.domain} --threads 20'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        output =[]
        try:
            for line in iter(dnsenum.stdout.readline, ''):
                if recon_obj.mode == "cli":
                    print(line.strip())
                output.append(line.strip())
            dnsenum.stdout.close()
            dnsenum.wait()

            if dnsenum.returncode != 0:
                error_output = dnsenum.stderr.read()
                print( f"Error: {error_output.strip()}")

        except Exception as e:
            print(f"Exception: {e}")
        delimeter()
        output = "".join(output)
        recon_obj.db_handler.store_scan_result(inspect.currentframe().f_code.co_name,output)

    def subdomain(self,recon_obj):
        ''' This fucntion perform subdomain enumeration and aims to find maximum subdomain '''
        recon_obj.db_handler.initialize_function(inspect.currentframe().f_code.co_name,recon_obj.scan_type,self.module)
        sublist3r = subprocess.run(shlex.split(f'sublist3r -t 10 -b -e google,yahoo,bing,baidu,ask -d {recon_obj.domain}'),text=True,capture_output=True)
        if recon_obj.mode == "cli":
            print(sublist3r.stdout)
            delimeter()
        
        recon_obj.db_handler.store_scan_result(inspect.currentframe().f_code.co_name,sublist3r.stdout)

    @staticmethod
    def run_dns(recon_obj):
        obj = DNS()
        obj.dig(recon_obj)
        obj.dnsenum(recon_obj)
        # obj.subdomain(recon_obj)
        

