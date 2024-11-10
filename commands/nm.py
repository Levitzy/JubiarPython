import base64
import json
from api.sendMessage import send_message
from Crypto.Cipher import AES

name = "nm"
description = "Decrypts the provided encrypted content."
admin_bot = False  # Set to True if this command requires admin access

# AES decryption function using ECB mode
def decrypt_aes_ecb_128(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted

# Function to parse configuration data from JSON
def parse_config(data):
    result = []

    for key, value in data.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                result.append(f"{sub_key.lower()} {sub_value}")
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    for sub_key, sub_value in item.items():
                        result.append(f"{sub_key.lower()} {sub_value}")
                else:
                    result.append(f"{key.lower()} {item}")
        else:
            result.append(f"{key.lower()} {value}")
    return result

# Main function to handle decryption and parsing
def handle_nm(encrypted_content, key):
    message = []

    try:
        encrypted_text = base64.b64decode(encrypted_content)
        decrypted_text = decrypt_aes_ecb_128(encrypted_text, key)
        decrypted_string = decrypted_text.rstrip(b"\x00").decode('utf-8')

        # Attempt to extract JSON data from the decrypted string
        json_match = None
        if "{" in decrypted_string and "}" in decrypted_string:
            json_match = decrypted_string[decrypted_string.find("{"):decrypted_string.rfind("}") + 1]

        if json_match:
            try:
                json_object = json.loads(json_match)
                message.extend(parse_config(json_object))
            except json.JSONDecodeError as e:
                message.append(f"Error parsing decrypted JSON: {e.msg}")
        else:
            message.append("No valid JSON found after decryption.")

    except Exception as e:
        message.append(f"Error during decryption: {str(e)}")

    return message

def execute(sender_id, message_text):
    # Base64-decoded key from `mIn.py`
    key = base64.b64decode("X25ldHN5bmFfbmV0bW9kXw==")

    # Extract encrypted content from message text
    try:
        encrypted_content = message_text.split(" ", 1)[1]
        decrypted_message = handle_nm(encrypted_content, key)
        response_text = "\n".join(decrypted_message) if decrypted_message else "Decryption yielded no content."
    except IndexError:
        response_text = "Error: No encrypted content provided. Usage: nm {input_encrypted_content}"

    send_message(sender_id, {"text": response_text})
