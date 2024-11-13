from flask import Flask, request, send_from_directory
from api.sendMessage import send_message
from api.adminCheck import is_admin
import os
import importlib
import glob
import re

app = Flask(__name__)
VERIFY_TOKEN = "jubiar"

# Load command modules
commands = {}
for command_file in glob.glob("commands/*.py"):
    command_name = os.path.basename(command_file)[:-3]
    command_module = importlib.import_module(f"commands.{command_name}")
    commands[command_module.name] = command_module

# Load file handlers from root/fileCmd/
file_handlers = {}
for handler_file in glob.glob("fileCmd/*.py"):
    handler_name = os.path.basename(handler_file)[:-3]
    file_extension = f".{handler_name}"  # Set the file extension based on filename
    handler_module = importlib.import_module(f"fileCmd.{handler_name}")
    
    # Register the handler for the specific file extension if handle_file function exists
    if hasattr(handler_module, 'handle_file'):
        file_handlers[file_extension] = handler_module.handle_file

def get_clean_extension(url):
    # Remove any query parameters
    clean_url = url.split('?')[0]
    # Extract and return the file extension
    return os.path.splitext(clean_url)[-1].lower()

@app.route('/')
def index():
    return send_from_directory('site', 'index.html')

@app.route('/webhook', methods=['GET'])
def verify():
    token = request.args.get("hub.verify_token")
    if request.args.get("hub.mode") == "subscribe" and token == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Verification failed", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    body = request.json
    if body['object'] == 'page':
        for entry in body['entry']:
            for event in entry.get('messaging', []):
                sender_id = event['sender']['id']

                # Handle text commands
                if event.get('message') and 'text' in event['message']:
                    message_text = event['message']['text'].strip()
                    command_name = message_text.split(' ')[0].lower()
                    command = commands.get(command_name)

                    if command:
                        if command.admin_bot and not is_admin(sender_id):
                            send_message(sender_id, {"text": "⚠️ You do not have permission to use this command."})
                        else:
                            command.execute(sender_id, message_text)
                    else:
                        send_message(sender_id, {"text": "Unrecognized command. Type 'help' for available options."})

                # Handle file attachments for fileCmd modules, with admin check
                elif event.get('message') and 'attachments' in event['message']:
                    for attachment in event['message']['attachments']:
                        if attachment['type'] == 'file':
                            if not is_admin(sender_id):
                                send_message(sender_id, {"text": "⚠️ You do not have permission to use this file handler."})
                                continue
                            
                            file_url = attachment['payload']['url']
                            file_extension = get_clean_extension(file_url)
                            handler_function = file_handlers.get(file_extension)
                            
                            if handler_function:
                                handler_function(sender_id, file_url)
                            else:
                                send_message(sender_id, {"text": f"No handler available for {file_extension} files."})

        return "EVENT_RECEIVED", 200
    return "Not Found", 404
