import requests
import os
from api.sendMessage import send_message

name = "shoti"
description = "Fetches a video using the Shoti API, downloads it, and sends it as a video attachment."
admin_bot = False

def execute(sender_id, message_text):
    if message_text.strip() == name:
        # Inform the user that the process has started
        send_message(sender_id, {"text": "Processing your video, please wait..."})

        try:
            # Request video details from Shoti API
            api_url = "https://shoti.kenliejugarap.com/getvideo.php?apikey=shoti-7eb71049889365e4d57c63fcb3e1d5e1bb80a178e4016bb48df704b0ed4f95798cb464105ae55c064bebb5d2470beed4c077a7bcf5f4b9673ecaaef349530bea2375588713cc819677428b042e9d665c85977c68cc"
            response = requests.get(api_url)
            response_data = response.json()

            if response_data["status"]:
                video_url = response_data["videoDownloadLink"]
                video_title = response_data["title"]
                tiktok_url = response_data["tiktokUrl"]
                temp_file_path = os.path.join(os.path.dirname(__file__), "shoti.mp4")

                # Download and save the video locally
                with requests.get(video_url, stream=True) as r:
                    r.raise_for_status()
                    with open(temp_file_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

                # Send the video as an attachment
                with open(temp_file_path, "rb") as video_file:
                    send_message(sender_id, {
                        "attachment": {
                            "type": "video",
                            "payload": {
                                "is_reusable": True
                            }
                        },
                        "filedata": {
                            "filename": "shoti.mp4",
                            "content": video_file,
                            "content_type": "video/mp4"
                        }
                    })

                # Send the video title and TikTok URL after the video is sent
                send_message(sender_id, {
                    "text": f"{video_title}\n\n{tiktok_url}\n\nCredits: Kenlie"
                })

                # Remove the temporary file after sending
                os.remove(temp_file_path)
            else:
                # No video found message
                send_message(sender_id, {"text": "Sorry, no video was found."})

        except requests.RequestException as e:
            # Error handling for request issues
            print("Error fetching, downloading, or sending the video:", e)
            send_message(sender_id, {"text": "An error occurred while fetching the video. Please try again later."})

        except Exception as e:
            # General exception handling
            print("Error:", e)
            send_message(sender_id, {"text": "An unexpected error occurred. Please try again later."})
