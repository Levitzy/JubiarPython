from api.sendMessage import send_message
import time

name = 'uptime'
description = 'Displays the bot\'s uptime.'
admin_bot = False

def execute(sender_id, message_text):
    start_time = time.time()
    
    uptime_seconds = int(time.time() - start_time)
    uptime_minutes = uptime_seconds // 60
    uptime_hours = uptime_minutes // 60
    
    response_message = {
        "text": f"I've been running for {uptime_hours} hours, {uptime_minutes % 60} minutes, and {uptime_seconds % 60} seconds."
    }
    send_message(sender_id, response_message)
