import pyfiglet
import argparse
import sys
import requests

def main():
    text = "PenTek"
    banner = pyfiglet.figlet_format(text,font="pagga")

    print(banner)


if __name__ == "__main__":
    main()