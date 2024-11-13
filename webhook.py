from flask import Flask, request, send_from_directory
from api.sendMessage import send_message
from api.adminCheck import is_admin
import os
import importlib
import glob

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

                # Handle file attachments based on extension
                elif event.get('message') and 'attachments' in event['message']:
                    for attachment in event['message']['attachments']:
                        if attachment['type'] == 'file':
                            file_url = attachment['payload']['url']
                            file_extension = os.path.splitext(file_url)[-1].lower()
                            handler_function = file_handlers.get(file_extension)
                            
                            if handler_function:
                                handler_function(sender_id, file_url)
                            else:
                                send_message(sender_id, {"text": f"No handler available for {file_extension} files."})

        return "EVENT_RECEIVED", 200
    return "Not Found", 404
