import requests
from api.sendMessage import send_message

name = "chost"
description = "Manage and process hosts."
admin_bot = False

hosts = {}

def add_host(sender_id, message_text):
    user_input = message_text.replace("chost add ", "").strip()
    new_hosts = [host.strip() for host in user_input.split(";") if host.strip()]
    
    for host in new_hosts:
        if host not in hosts:
            hosts[host] = "Pending"
    send_message(sender_id, {"text": f"Added hosts: {', '.join(new_hosts)}"})

def start_processing(sender_id):
    response_text = ""
    for host in hosts.keys():
        try:
            response = requests.get(f"http://{host}")
            ip = response.raw._connection.sock.getpeername()[0]  # Get IP of the host
            hosts[host] = f"Status: {response.status_code}, IP: {ip}"
        except Exception as e:
            hosts[host] = f"Error: {e}"
    
    for host, status in hosts.items():
        response_text += f"Host: {host}\n{status}\n\n"

    send_message(sender_id, {"text": response_text.strip()})

def delete_host(sender_id, message_text):
    host_to_delete = message_text.replace("chost del ", "").strip()
    if host_to_delete in hosts:
        del hosts[host_to_delete]
        send_message(sender_id, {"text": f"Deleted host: {host_to_delete}"})
    else:
        send_message(sender_id, {"text": f"Host {host_to_delete} not found."})

def show_hosts(sender_id):
    if not hosts:
        send_message(sender_id, {"text": "No hosts added yet."})
    else:
        response_text = "Current Hosts:\n"
        for host, status in hosts.items():
            response_text += f"Host: {host}\n{status}\n\n"
        send_message(sender_id, {"text": response_text.strip()})

def execute(sender_id, message_text):
    if message_text.startswith("chost add "):
        add_host(sender_id, message_text)
    elif message_text == "chost start":
        start_processing(sender_id)
    elif message_text.startswith("chost del "):
        delete_host(sender_id, message_text)
    elif message_text == "chost info":
        show_hosts(sender_id)
    else:
        send_message(sender_id, {"text": "Unknown command. Try: chost add, chost start, chost del, chost info"})
