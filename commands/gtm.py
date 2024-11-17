from sendMessage import send_message
import time
import subprocess
import threading

# Command metadata
name = "gtm"
description = "Manages DNS and Nameservers, starts/stops process, and displays thread count."
admin_bot = False

# Global variables
dns_ips = []
name_servers = []
loop_delay = 5
process_running = False
check_count = 1

def check_dns_and_nameservers():
    global check_count
    print("\033[95m┌────────────────────────────────────────────────┐")
    print("\033[95m│\033[96m  DNS Status Check Results  \033[95m│")
    print("\033[95m├────────────────────────────────────────────────┤")

    for dns in dns_ips:
        for ns in name_servers:
            try:
                result = subprocess.check_output(
                    ["dig", f"@{dns}", ns, "+short"], universal_newlines=True
                ).strip()
                if result:
                    status = "\033[92mSuccess\033[0m"
                else:
                    status = "\033[91mFailed\033[0m"
            except subprocess.CalledProcessError:
                status = "\033[91mFailed\033[0m"

            print(f"\033[95m│  \033[0mDNS IP: {dns}\033[0m")
            print(f"\033[95m│  \033[0mNameServer: {ns}\033[0m")
            print(f"\033[95m│  \033[0mStatus: {status}\033[0m")

    print("\033[95m├────────────────────────────────────────────────┤")
    print(f"\033[95m│  \033[96mCheck count: {check_count}\033[0m")
    print(f"\033[95m│  Loop Delay: {loop_delay} seconds  \033[0m")
    print("\033[95m└────────────────────────────────────────────────┘")
    check_count += 1

def countdown():
    for i in range(10, 0, -1):
        print(f"Checking starts in {i} seconds...")
        time.sleep(1)

def start_check():
    global process_running
    if not dns_ips or not name_servers:
        print("Please set DNS IPs and NameServers before starting the process.")
        return

    if process_running:
        print("Process is already running.")
        return

    process_running = True
    print("Starting the DNS and NameServer check process...")
    countdown()
    print("\033[H\033[J")  # Clear screen
    while process_running:
        check_dns_and_nameservers()
        time.sleep(loop_delay)

def stop_check():
    global process_running
    if process_running:
        process_running = False
        print("Stopping the DNS and NameServer check process...")
    else:
        print("No process is currently running.")

def execute(sender_id, message_text):
    global dns_ips, name_servers, loop_delay

    try:
        args = message_text.split()
        if len(args) < 2:
            send_message(sender_id, {"text": "Invalid command. Use: gtm [dns/ns/start/stop/info] {arguments}"})
            return

        command = args[1].lower()
        if command == "dns":
            dns_ips = args[2:]
            send_message(sender_id, {"text": f"DNS IPs set to: {', '.join(dns_ips)}"})
        elif command == "ns":
            name_servers = args[2:]
            send_message(sender_id, {"text": f"NameServers set to: {', '.join(name_servers)}"})
        elif command == "start":
            thread = threading.Thread(target=start_check)
            thread.start()
            send_message(sender_id, {"text": "Process started successfully."})
        elif command == "stop":
            stop_check()
            send_message(sender_id, {"text": "Process stopped successfully."})
        elif command == "info":
            send_message(sender_id, {"text": f"Check count: {check_count}, Loop Delay: {loop_delay} seconds."})
        else:
            send_message(sender_id, {"text": f"Unknown command: {command}"})
    except Exception as e:
        send_message(sender_id, {"text": f"Error executing command: {e}"})
