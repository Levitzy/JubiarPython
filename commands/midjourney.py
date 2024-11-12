from api.sendMessage import send_message
import requests
import re

name = "midjourney"
description = "Fetches and formats response from the specified MidJourney API using user input."
admin_bot = False  # Does not require admin privileges

def execute(sender_id, message_text):
    # Extract user input by removing the command prefix "midjourney"
    user_input = message_text.replace("midjourney", "", 1).strip()
    
    # Check if user provided input
    if not user_input:
        send_message(sender_id, {"text": "Please provide a prompt after the 'midjourney' command."})
        return
    
    # Call the API with the extracted user input
    api_url = f"https://api.kenliejugarap.com/midijourney/?question={user_input}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        
        # Extract response data
        data = response.json().get('response', '')
        
        # Clean markdown symbols from the response
        cleaned_data = re.sub(r'[\*\_`>|]', '', data)
        
        # Remove any trailing or leading ```
        cleaned_data = re.sub(r'(^```|```$)', '', cleaned_data)

        # Send the cleaned response to the user
        send_message(sender_id, {"text": cleaned_data})
    
    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching data: {e}"
        send_message(sender_id, {"text": error_message})
