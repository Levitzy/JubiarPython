from api.sendMessage import send_message

name = "uid"
description = "Returns the user ID of the sender."
admin_bot = False  # Set to True if this command requires admin access

def execute(sender_id, message_text):
    response_text = f"Your user ID is: {sender_id}"
    send_message(sender_id, {"text": response_text})
