import pyfiglet
import argparse

from phases.recon import Recon
from phases.scanning import Scanning
from phases.exploitaion import Exploitation
from phases.web import WebExploitation
from database.mongodb_handler import MongoDBHandler

def initialize_database(domain) -> MongoDBHandler:
    '''Initialize database to store scan result'''
    db_handler = MongoDBHandler(domain)
    db_handler.store_metadata()
    db_handler.update_scan_status("running")
    return db_handler

def main():
    parser = argparse.ArgumentParser(description="PenTek CLI")
    parser.add_argument('--domain', type=str, help='Domain to scan')
    parser.add_argument('--mode', type=str, default='cli', choices=['cli', 'web'], help='Mode to run')
    parser.add_argument('--scan_type', type=str, default='full', help='Type of scan to run {recon,scanning,full}')
    args = parser.parse_args()

    text = "PenTek"
    banner = pyfiglet.figlet_format(text,font="pagga")
    print(banner)

    domain = args.domain
    if args.mode == 'cli' and not domain:
        domain = input("Enter the domain: ")
        db_handler = initialize_database(domain)
        args.scan_type = input("Enter Scan type: ")

    if not domain:
        print("Domain is required.")
        return

    if args.scan_type == 'recon':
        Recon.recon_run(domain, db_handler, args.mode)
    elif args.scan_type == 'scanning':
        Scanning.run_scanning(domain,db_handler, args.mode)
    else:
        Recon.recon_run(domain, db_handler, args.mode)
        Scanning.run_scanning(domain,db_handler, args.mode)
        Exploitation.run_exploitation(domain,db_handler,args.mode)
        WebExploitation.run_all(domain,db_handler,args.mode)
        

    db_handler.update_scan_status("completed")

if __name__ == "__main__":
    main()
