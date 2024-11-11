from api.sendMessage import send_message
import json
import hashlib
from Crypto.Cipher import AES
from base64 import b64decode, b64encode
import os

name = "sks"
description = "Decrypts user-provided encrypted JSON content and sends it as a document attachment."
admin_bot = True

config_keys = [...]  # List of decryption keys as in the original code

def aes_decrypt(data, key, iv):
    aes_instance = AES.new(b64decode(key), AES.MODE_CBC, b64decode(iv))
    decrypted_data = aes_instance.decrypt(b64decode(data))
    return decrypted_data.decode('utf-8').rstrip('\x10')

def md5crypt(data):
    return hashlib.md5(data.encode()).hexdigest()

def clean_json_data(data):
    start = data.find('{')
    end = data.rfind('}') + 1
    if start == -1 or end == -1:
        raise ValueError("Failed to locate JSON data")
    return data[start:end]

def decrypt_data(data, iv, version):
    for key in config_keys:
        try:
            aes_key = b64encode(md5crypt(key + " " + str(version)).encode()).decode()
            decrypted_data = aes_decrypt(data, aes_key, iv)
            return clean_json_data(decrypted_data)
        except Exception:
            continue
    raise Exception("No valid key found")

def format_output(data):
    lines = []
    for key, value in data.items():
        if key == "message":
            continue  # Skip the "message" field
        if isinstance(value, dict):
            lines.append(f"🔑 {key}:")
            lines.extend(format_output(value))
        elif isinstance(value, list):
            lines.append(f"🔑 {key}: [{', '.join(map(str, value))}]")
        else:
            lines.append(f"🔑 {key}: {value}")
    return lines

def execute(sender_id, message_text):
    try:
        encrypted_content = message_text.split(" ", 1)[1]
        content_json = json.loads(encrypted_content)
        data = content_json['d']
        version = content_json['v']
        iv = data.split(".")[1]
        encrypted_part = data.split(".")[0]

        decrypted_data = decrypt_data(encrypted_part, iv, version)
        json_data = json.loads(decrypted_data)

        formatted_output = ["🎉 Decrypted Content:"]
        formatted_output.extend(format_output(json_data))
        formatted_content = "\n".join(formatted_output)
        
        # Save the decrypted content to a temporary file
        temp_file_path = os.path.join(os.path.dirname(__file__), "decrypted.txt")
        with open(temp_file_path, "w") as file:
            file.write(formatted_content)

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

    except Exception as e:
        error_message = f"[ERROR] An error occurred during decryption: {e}"
        send_message(sender_id, {"text": error_message})
