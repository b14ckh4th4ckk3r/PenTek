import subprocess


def dnsenum(domain):

    dnsenum = subprocess.run(f'dnsenum {domain} q-type * q-class *',shell=True,text=True)
    print(dnsenum.stdout)