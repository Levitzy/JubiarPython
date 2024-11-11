import os
from api.sendMessage import send_message

name = "help"
description = "Lists all available commands."
admin_bot = False  # Doesn't require admin privileges

def execute(sender_id, message_text):
    # Path to the commands folder
    commands_folder = os.path.join(os.path.dirname(__file__), "commands")
    # List all .py files in the commands folder
    command_files = [f for f in os.listdir(commands_folder) if f.endswith(".py")]

    # Prepare the message
    command_list = "\n".join(f"- {command.replace('.py', '')}" for command in command_files)
    response_text = "Here are the available commands:\n" + command_list

    # Send the message
    send_message(sender_id, {"text": response_text})
