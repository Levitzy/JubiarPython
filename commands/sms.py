from api.sendMessage import send_message
import requests

name = "sms"
description = "Send SMS using the FreeSMS API."
admin_bot = False

def execute(sender_id, message_text):
    try:
        # Parse the input format: "sms number|message"
        if "|" not in message_text:
            raise ValueError("Invalid format. Use: sms number|message")

        # Split input into number and message
        _, payload = message_text.split(" ", 1)
        number, sms_message = payload.split("|", 1)

        # Trim whitespace
        number = number.strip()
        sms_message = sms_message.strip()

        # Construct API URL
        api_url = f"https://api.kenliejugarap.com/freesmslbc/?number={number}&message={sms_message}"

        # Call the SMS API
        response = requests.get(api_url)
        response.raise_for_status()

        # Send feedback to the user
        api_response = response.json()
        if api_response.get("status") == "success":
            send_message(sender_id, {"text": f"SMS sent successfully to {number}."})
        else:
            error_msg = api_response.get("message", "Unknown error")
            send_message(sender_id, {"text": f"Failed to send SMS. Error: {error_msg}"})

    except ValueError as e:
        send_message(sender_id, {"text": f"Error: {str(e)}"})
    except requests.exceptions.RequestException as e:
        send_message(sender_id, {"text": f"Network error while sending SMS: {str(e)}"})
    except Exception as e:
        send_message(sender_id, {"text": f"Unexpected error: {str(e)}"})
