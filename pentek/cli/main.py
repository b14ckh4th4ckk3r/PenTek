import pyfiglet
import argparse
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from phases import recon

def main():
    text = "PenTek"
    banner = pyfiglet.figlet_format(text,font="pagga")
    print(banner)
    recon.recon_run("testfire.net")





if __name__ == "__main__":
    main()