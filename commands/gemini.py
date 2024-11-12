from api.sendMessage import send_message
import requests
import re

name = "gemini"
description = "Fetches an image response from the specified Gemini API using user input and an image URL."
admin_bot = False  # Does not require admin privileges

def execute(sender_id, message_text, attachments=None):
    # Extract user input by removing the command prefix "gemini"
    user_input = message_text.replace("gemini", "", 1).strip()
    
    # Check if user provided both input and an image
    if not user_input:
        send_message(sender_id, {"text": "Please provide a prompt after the 'gemini' command."})
        return
    if not attachments or "image" not in attachments:
        send_message(sender_id, {"text": "Please attach an image along with the 'gemini' command."})
        return
    
    # Extract the URL of the user's image
    user_image_url = attachments["image"][0]["url"]

    # Call the API with the extracted user input and image URL
    api_url = f"https://joshweb.click/gemini?prompt={user_input}&url={user_image_url}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        
        # Extract the 'gemini' value (the image URL) from the response
        gemini_image_url = response.json().get('gemini', '')
        
        # Check if gemini_image_url is empty
        if not gemini_image_url:
            send_message(sender_id, {"text": "No image response received from the API."})
            return

        # Send the image back to the user
        message = {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": gemini_image_url,
                    "is_reusable": True
                }
            }
        }
        send_message(sender_id, message)
    
    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching data: {e}"
        send_message(sender_id, {"text": error_message})
