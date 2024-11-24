import requests
from api.sendMessage import send_message
import os
import tempfile

name = "fbdl"
description = "Downloads a video from a provided Facebook video link."
admin_bot = False

def execute(sender_id, message_text):
    temp_file_path = None
    try:
        # Extract video link from the message_text
        video_link = message_text.strip()
        
        # Make API call to get the video download link
        api_url = f"https://api.kenliejugarap.com/fbdl/?videoUrl={video_link}"
        response = requests.get(api_url)
        response_data = response.json()
        
        if not response_data.get("status", False):
            send_message(sender_id, {"text": "Failed to fetch the video. Please check the link and try again."})
            return
        
        video_url = response_data["response"]
        
        # Download the video temporarily
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, "video.mp4")
        
        video_response = requests.get(video_url, stream=True)
        video_response.raise_for_status()
        
        with open(temp_file_path, "wb") as temp_file:
            for chunk in video_response.iter_content(chunk_size=8192):
                temp_file.write(chunk)
        
        # Send the video as an attachment
        message = {
            "attachment": {
                "type": "file",
                "payload": {}
            },
            "filedata": {
                "filename": "video.mp4",
                "content": open(temp_file_path, "rb"),
                "content_type": "video/mp4"
            }
        }
        send_message(sender_id, message)
        
        # Send a follow-up message with the download link
        download_message = f"Download link: {video_url}"
        send_message(sender_id, {"text": download_message})
    
    except Exception as e:
        # Handle errors
        send_message(sender_id, {"text": f"An error occurred: {e}"})
    
    finally:
        # Clean up the temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
