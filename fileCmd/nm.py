import base64
from Crypto.Cipher import AES
from api.sendMessage import send_message
import requests
import json
import os

admin_bot = True

# Constants
DECRYPTION_KEY = base64.b64decode("X25ldHN5bmFfbmV0bW9kXw==")  # Replace with your decryption key

def decrypt_aes_ecb_128(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted

def parse_config(data):
    result = []
    for key, value in data.items():
        if key.lower() == "note":
            continue
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if sub_key.lower() != "note":
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

def handle_file(sender_id, file_url):
    try:
        # Download the file content
        file_content = download_file_content(file_url)
        
        # Decode and decrypt the content
        encrypted_content = base64.b64decode(file_content)
        decrypted_text = decrypt_aes_ecb_128(encrypted_content, DECRYPTION_KEY).rstrip(b"\x00").decode('utf-8')

        message = []
        # Check if the decrypted text contains JSON and parse it
        if "{" in decrypted_text and "}" in decrypted_text:
            json_match = decrypted_text[decrypted_text.find("{"):decrypted_text.rfind("}") + 1]
            try:
                json_object = json.loads(json_match)
                message.extend(parse_config(json_object))
            except json.JSONDecodeError as e:
                message.append(f"Error parsing decrypted JSON: {e.msg}")
        else:
            message.append("No valid JSON found after decryption.")
        
        # Prepare the response message
        decrypted_content = "\n".join(message) if message else "Decryption yielded no content."
        
        # Send the decryption result as a message
        send_message(sender_id, {"text": decrypted_content})

        # Save and send the result as a document
        temp_file_path = os.path.join(os.path.dirname(__file__), "decrypted.txt")
        with open(temp_file_path, "w", encoding="utf-8") as file:
            file.write(decrypted_content)

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

        # Remove the temporary file
        os.remove(temp_file_path)

    except Exception as e:
        send_message(sender_id, {"text": f"Error during decryption: {str(e)}"})

def download_file_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Failed to download file content: {e}")
        return None
