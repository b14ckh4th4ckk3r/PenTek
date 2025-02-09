import subprocess


def dnsenumeration(domain):


    dig = subprocess.run(f'dig {domain} q-type * q-class *',shell=True,text=True)
    print(dig.stdout)

    dnsenum = subprocess.run(f'dnsenum {domain}',shell=True,text=True)
    print(dnsenum.stdout)
