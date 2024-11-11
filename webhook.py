from flask import Flask, request, send_from_directory
from api.sendMessage import send_message
from api.adminCheck import is_admin
import os
import importlib
import glob

app = Flask(__name__)
VERIFY_TOKEN = "jubiar"

commands = {}
for command_file in glob.glob("commands/*.py"):
    command_name = os.path.basename(command_file)[:-3]
    command_module = importlib.import_module(f"commands.{command_name}")
    commands[command_module.name] = command_module

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
        return "EVENT_RECEIVED", 200
    return "Not Found", 404
