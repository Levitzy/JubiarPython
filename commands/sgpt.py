from api.sendMessage import send_message
import requests
import re

name = "sgpt"
description = "Fetches and formats response from the specified SearchGPT API using user input."
admin_bot = False  # Does not require admin privileges

def execute(sender_id, message_text):
    # Extract user input by removing the command prefix "sgpt"
    user_input = message_text.replace("sgpt", "", 1).strip()
    
    # Check if user provided input
    if not user_input:
        send_message(sender_id, {"text": "Please provide a question after the 'sgpt' command."})
        return
    
    # Call the API with the extracted user input
    api_url = f"https://api.kenliejugarap.com/searchgpt/?question={user_input}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        
        # Extract response data
        response_data = response.json()
        content = response_data.get('choices', [{}])[0].get('message', {}).get('content', "No response available.")
        
        # Clean markdown symbols from the response
        cleaned_data = re.sub(r'[\*\_`>|]', '', content)
        
        # Remove any trailing or leading ```
        cleaned_data = re.sub(r'(^```|```$)', '', cleaned_data)

        # Ensure non-empty response before sending
        if not cleaned_data.strip():
            cleaned_data = "The API returned an empty response. Please try again."

        # Send the cleaned response to the user
        send_message(sender_id, {"text": cleaned_data})
    
    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching data: {e}"
        send_message(sender_id, {"text": error_message})
    except ValueError:
        send_message(sender_id, {"text": "Error parsing API response. Please contact support."})
