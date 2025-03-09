import pyfiglet
import argparse
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from phases.recon import Recon
# from phases.scanning import scanning
from database.mongodb_handler import MongoDBHandler

def initialize_database(domain) -> MongoDBHandler:
    '''Initialize database to store scan result'''
    db_handler = MongoDBHandler(domain)
    # db_handler.store_metadata()
    db_handler.update_scan_status("running")
    return db_handler

def main():
    text = "PenTek"
    banner = pyfiglet.figlet_format(text,font="pagga")
    print(banner)
    domain = input("Enter the domain: ")
    db_handler = initialize_database(domain)
    Recon.recon_run(domain,db_handler,"cli")
    # scanning.run_scanning(domain,db_handler,"cli")
    db_handler.update_scan_status("Completed")





if __name__ == "__main__":
    main()