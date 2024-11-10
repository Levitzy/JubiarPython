import requests

# Read PAGE_ACCESS_TOKEN from token.txt
with open('token.txt', 'r') as file:
    PAGE_ACCESS_TOKEN = file.read().strip()

def send_message(recipient_id, message):
    url = f"https://graph.facebook.com/v11.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": message,
        "messaging_type": "RESPONSE"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print("Failed to send message:", response.text)
    return response.json()
