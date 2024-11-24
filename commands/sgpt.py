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
        # Fetch and validate response
        response = requests.get(api_url)
        response.raise_for_status()
        api_data = response.json()

        # Extract and clean the response content
        data_content = api_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        cleaned_data = re.sub(r'[\*\_`>|]', '', data_content)  # Remove markdown symbols
        cleaned_data = re.sub(r'(^```|```$)', '', cleaned_data)  # Remove code block symbols

        # Send the cleaned response to the user
        if cleaned_data:
            send_message(sender_id, {"text": cleaned_data})
        else:
            send_message(sender_id, {"text": "The API did not return any meaningful content."})

    except requests.exceptions.RequestException as e:
        send_message(sender_id, {"text": f"Error fetching data from API: {str(e)}"})

    except ValueError as e:
        send_message(sender_id, {"text": f"Error processing API response: {str(e)}"})
