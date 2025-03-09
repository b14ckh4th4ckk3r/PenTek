


import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import subprocess

app = FastAPI()

def run_scan(target):
    scan_script = "/home/kali/Desktop/PenTek/pentek/phases/scanning.py"
    process = subprocess.Popen(
        ["python3", scan_script, target, "web"], 
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    for line in iter(process.stdout.readline, ''):
        # Identify tool name based on output patterns (Example: Checking for "Nmap" in output)
        if "Nmap" in line:
            tool_name = "Nmap"
        elif "Nikto" in line:
            tool_name = "Nikto"
        elif "SQLMap" in line:
            tool_name = "SQLMap"
        else:
            tool_name = "Unknown"

        # Send output as JSON
        yield f"{json.dumps({'tool': tool_name, 'output': line.strip()})}\n"

@app.get("/run_scan/")
async def run_scan_stream(target: str):
    return StreamingResponse(run_scan(target), media_type="text/event-stream")
