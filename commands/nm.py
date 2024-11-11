import base64
import json
from api.sendMessage import send_message
from Crypto.Cipher import AES
import os

name = "nm"
description = "Decrypts the provided encrypted content and sends it as a document attachment."
admin_bot = True  # Set to True if this command requires admin access

def decrypt_aes_ecb_128(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted

def parse_config(data):
    result = []
    for key, value in data.items():
        if key.lower() == "note":
            continue  # Skip any "note" keys
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if sub_key.lower() != "note":  # Exclude nested "note" keys
                    result.append(f"{sub_key.lower()} {sub_value}")
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    for sub_key, sub_value in item.items():
                        if sub_key.lower() != "note":
                            result.append(f"{sub_key.lower()} {sub_value}")
                else:
                    result.append(f"{key.lower()} {item}")
        else:
            result.append(f"{key.lower()} {value}")
    return result

def handle_nm(encrypted_content, key):
    message = []
    try:
        encrypted_text = base64.b64decode(encrypted_content)
        decrypted_text = decrypt_aes_ecb_128(encrypted_text, key)
        decrypted_string = decrypted_text.rstrip(b"\x00").decode('utf-8')

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
    key = base64.b64decode("X25ldHN5bmFfbmV0bW9kXw==")
    try:
        encrypted_content = message_text.split(" ", 1)[1]
        decrypted_message = handle_nm(encrypted_content, key)
        if decrypted_message:
            decrypted_content = "\n".join(decrypted_message)
        else:
            decrypted_content = "Decryption yielded no content."
        
        # Save the decrypted content to a temporary file
        temp_file_path = os.path.join(os.path.dirname(__file__), "decrypted.txt")
        with open(temp_file_path, "w") as file:
            file.write(decrypted_content)

        # Send the document as an attachment
        with open(temp_file_path, "rb") as file:
            send_message(sender_id, {
                "attachment": {
                    "type": "file",
                    "payload": {}
                },
                "filedata": {
                    "filename": "decrypted.txt",
                    "content": file,
                    "content_type": "text/plain"
                }
            })

        # Remove the temporary file after sending
        os.remove(temp_file_path)

    except IndexError:
        send_message(sender_id, {"text": "Error: No encrypted content provided. Usage: nm {input_encrypted_content}"})
