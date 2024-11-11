import os
from api.sendMessage import send_message

name = "help"
description = "Lists all available commands with a modern design and admin indication."
admin_bot = False

def execute(sender_id, message_text):
    base_path = os.path.dirname(os.path.dirname(__file__))
    commands_folder = os.path.join(base_path, "commands")
    
    try:
        command_files = [f for f in os.listdir(commands_folder) if f.endswith(".py")]
        command_list = []
        
        for command_file in command_files:
            command_name = command_file.replace('.py', '')
            module = __import__(f"commands.{command_name}", fromlist=["admin_bot"])
            admin_status = "🔒 Admin Only" if getattr(module, "admin_bot", False) else "🔓 User Accessible"
            command_list.append(f"• **{command_name.capitalize()}** - {admin_status}")

        response_text = (
            "🌐 **Available Commands** 🌐\n"
            "Here’s a list of commands you can use:\n\n" + 
            "\n".join(command_list) +
            "\n\nUse these commands to interact with the bot. Commands marked with 🔒 require admin privileges."
        )
        
        send_message(sender_id, {"text": response_text})
    
    except FileNotFoundError:
        error_text = "🚫 Error: Commands folder not found."
        send_message(sender_id, {"text": error_text})

    except Exception as e:
        error_text = f"⚠️ An error occurred: {str(e)}"
        send_message(sender_id, {"text": error_text})
