from flask import Flask, request, send_from_directory
from api.sendMessage import send_message
from api.adminCheck import is_admin
from commands import hi  # Updated import path
import os

app = Flask(__name__)
VERIFY_TOKEN = "jubiar"

# Load commands dynamically (add each new command here)
commands = {
    hi.name: hi
}

@app.route('/')
def index():
    return send_from_directory('site', 'index.html')

@app.route('/webhook', methods=['GET'])
def verify():
    # Verification route
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
                        # Check for admin rights if the command requires it
                        if getattr(command, 'admin_bot', False) and not is_admin(sender_id):
                            send_message(sender_id, {"text": "⚠️ You do not have permission to use this command."})
                        else:
                            command.execute(sender_id, message_text)
                    else:
                        send_message(sender_id, {"text": "Unrecognized command. Type 'help' for available options."})
        return "EVENT_RECEIVED", 200
    return "Not Found", 404
