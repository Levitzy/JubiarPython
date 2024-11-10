import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os

# Read PAGE_ACCESS_TOKEN from token.txt
with open(os.path.join(os.path.dirname(__file__), '../token.txt'), 'r') as file:
    PAGE_ACCESS_TOKEN = file.read().strip()

# Split long messages into chunks of max 2000 characters
def split_message(text, max_length=2000):
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def send_typing_indicator(recipient_id, action):
    url = f"https://graph.facebook.com/v11.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    response = requests.post(url, json={
        "recipient": {"id": recipient_id},
        "sender_action": action
    })
    if response.status_code != 200:
        print(f"Failed to send typing indicator: {response.text}")

def send_message(recipient_id, message):
    url = f"https://graph.facebook.com/v21.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"

    try:
        # Send typing indicator
        send_typing_indicator(recipient_id, 'typing_on')

        # Handle file attachments
        if "filedata" in message:
            form_data = MultipartEncoder(
                fields={
                    "recipient": json.dumps({"id": recipient_id}),
                    "message": json.dumps({"attachment": message["attachment"]}),
                    "filedata": (message["filedata"]["filename"], message["filedata"]["content"], message["filedata"]["content_type"])
                }
            )
            response = requests.post(url, data=form_data, headers={"Content-Type": form_data.content_type})
            response.raise_for_status()

        # Handle text messages and long messages
        elif "text" in message:
            if len(message["text"]) > 2000:
                message_chunks = split_message(message["text"])
                for chunk in message_chunks:
                    data = {
                        "recipient": {"id": recipient_id},
                        "message": {"text": chunk}
                    }
                    response = requests.post(url, json=data)
                    response.raise_for_status()
            else:
                data = {
                    "recipient": {"id": recipient_id},
                    "message": {"text": message["text"]}
                }
                response = requests.post(url, json=data)
                response.raise_for_status()

        # Handle any other errors
        print("Message sent successfully.")

    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        # Send error message to user
        error_message = str(e)
        requests.post(url, json={
            "recipient": {"id": recipient_id},
            "message": {"text": f"Error: {error_message}"}
        })

    finally:
        # Turn off typing indicator
        send_typing_indicator(recipient_id, 'typing_off')
