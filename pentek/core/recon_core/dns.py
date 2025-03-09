import subprocess
import shlex

def dnsenumeration(domain:str):
    ''' This fucntion perform basic dns enumeration. '''
    
    output =[]
    dig = subprocess.run(shlex.split(f'dig all +short {domain} q-type * q-class *'),capture_output=True,text=True)
    
    yield dig.stdout

    dnsenum = subprocess.Popen(shlex.split(f'dnsenum {domain} --threads 20'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)

    try:
        for line in iter(dnsenum.stdout.readline, ''):
            yield line.strip()
        dnsenum.stdout.close()
        dnsenum.wait()

        if dnsenum.returncode != 0:
            error_output = dnsenum.stderr.read()
            yield f"Error: {error_output.strip()}"

    except Exception as e:
        yield f"Exception: {e}"

def subdomain(domain):
    ''' This fucntion perform subdomain enumeration and aims to find maximum subdomain '''
    sublist3r = subprocess.run(shlex.split(f'sublist3r -t 10 -b -e google,yahoo,bing,baidu,ask -d {domain}'),text=True)
    return sublist3r

