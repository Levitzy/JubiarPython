from api.sendMessage import send_message
import requests
import tempfile
import os

name = "gemini"
description = "Fetches an image response from the specified Gemini API using user input, after the user has uploaded an image."
admin_bot = False  # Does not require admin privileges

# Dictionary to store temporary file paths for each user
user_image_storage = {}

def store_image(sender_id, image_url):
    """Download and store the user's image temporarily."""
    try:
        # Download the image and save it as a temporary file
        image_response = requests.get(image_url)
        image_response.raise_for_status()

        # Create a temporary file to save the downloaded image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image_file:
            temp_image_file.write(image_response.content)
            temp_image_file_path = temp_image_file.name
        
        # Store the file path in user_image_storage for later use
        user_image_storage[sender_id] = temp_image_file_path
        send_message(sender_id, {"text": "Image saved! Now, please use 'gemini {your_prompt}' to generate a response."})

    except requests.exceptions.RequestException as e:
        error_message = f"Error saving image: {e}"
        send_message(sender_id, {"text": error_message})

def execute(sender_id, message_text, attachments=None):
    # If there is an image attachment, save it temporarily
    if attachments and "image" in attachments:
        image_url = attachments["image"][0]["url"]
        store_image(sender_id, image_url)
        return
    
    # If the command is invoked without an image attachment, check if user input is provided
    user_input = message_text.replace("gemini", "", 1).strip()
    
    # Check if user provided input for gemini command
    if not user_input:
        send_message(sender_id, {"text": "Please provide a prompt after the 'gemini' command."})
        return
    
    # Check if the user has previously uploaded an image
    if sender_id not in user_image_storage:
        send_message(sender_id, {"text": "Please upload an image first before using the 'gemini' command with a prompt."})
        return
    
    # Retrieve the stored image path
    temp_image_file_path = user_image_storage.pop(sender_id)

    try:
        # Prepare to upload the image file to the API with user prompt
        api_url = "https://joshweb.click/gemini"
        with open(temp_image_file_path, 'rb') as image_file:
            files = {'url': image_file}
            data = {'prompt': user_input}
            response = requests.post(api_url, files=files, data=data)
            response.raise_for_status()
        
        # Extract the 'gemini' value (the generated image URL) from the response
        gemini_image_url = response.json().get('gemini', '')
        
        # Check if gemini_image_url is empty
        if not gemini_image_url:
            send_message(sender_id, {"text": "No image response received from the API."})
            return

        # Send the generated image back to the user
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
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_image_file_path):
            os.remove(temp_image_file_path)
