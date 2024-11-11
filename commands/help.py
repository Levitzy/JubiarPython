import os
from api.sendMessage import send_message

name = "help"
description = "Lists all available commands with admin privileges indication."
admin_bot = False  # Doesn't require admin privileges

def execute(sender_id, message_text):
    # Absolute path to the commands folder
    base_path = os.path.dirname(os.path.dirname(__file__))  # Navigate to the base directory
    commands_folder = os.path.join(base_path, "commands")
    
    try:
        # List all .py files in the commands folder
        command_files = [f for f in os.listdir(commands_folder) if f.endswith(".py")]
        command_list = []
        
        for command_file in command_files:
            command_name = command_file.replace('.py', '')
            # Dynamically import each command module to check admin privileges
            module = __import__(f"commands.{command_name}", fromlist=["admin_bot"])
            admin_status = "Admin Only" if getattr(module, "admin_bot", False) else "User Accessible"
            command_list.append(f"- {command_name} ({admin_status})")

        # Join the list into a formatted message
        response_text = "Here are the available commands:\n" + "\n".join(command_list)
        
        # Send the message
        send_message(sender_id, {"text": response_text})
    
    except FileNotFoundError:
        # Handle the case where the commands folder is missing
        error_text = "Error: Commands folder not found."
        send_message(sender_id, {"text": error_text})

    except Exception as e:
        # Catch other potential errors
        error_text = f"An error occurred: {str(e)}"
        send_message(sender_id, {"text": error_text})
