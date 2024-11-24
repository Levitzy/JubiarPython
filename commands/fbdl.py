import requests
from api.sendMessage import send_message

name = "fbdl"
description = "Downloads a video from a provided Facebook video link."
admin_bot = False

def execute(sender_id, message_text):
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
        
        # Send the video directly as an attachment
        message = {
            "attachment": {
                "type": "video",
                "payload": {
                    "url": video_url,
                    "is_reusable": True
                }
            }
        }
        send_message(sender_id, message)
        
        # Send a follow-up message with the download link
        download_message = f"Download link: {video_url}"
        send_message(sender_id, {"text": download_message})
    
    except Exception as e:
        # Handle errors
        send_message(sender_id, {"text": f"An error occurred: {e}"})
