import os
import json
from hashlib import md5
from Crypto.Cipher import AES
from base64 import b64decode, b64encode
from api.sendMessage import send_message  # Assuming send_message is in sendMessage.py

name = "sks"
description = "Decrypts the provided encrypted content using predefined keys."
admin_bot = True

# List of keys from the original JavaScript file
config_keys = [
    "162exe235948e37ws6d057d9d85324e2", "dyv35182!", "dyv35224nossas!!",
    "662ede816988e58fb6d057d9d85605e0", "962exe865948e37ws6d057d4d85604e0",
    "175exe868648e37wb9x157d4l45604l0", "c7-YOcjyk1k", "Wasjdeijs@/ÇPãoOf231#$%¨&*()_qqu&iJo>ç",
    # Additional keys omitted for brevity
]

def aes_decrypt(data, key, iv):
    cipher = AES.new(b64decode(key), AES.MODE_CBC, b64decode(iv))
    decrypted = cipher.decrypt(b64decode(data))
    return decrypted.rstrip(b'\x10').decode('utf-8')  # Assuming PKCS#7 padding

def md5crypt(data):
    return md5(data.encode()).hexdigest()

def decrypt_data(data, version):
    for key in config_keys:
        try:
            encryption_key = b64encode(md5crypt(key + " " + version).encode()).decode('utf-8')
            iv, content = data.split('.')
            return aes_decrypt(content, encryption_key, iv)
        except Exception as e:
            print(f"Trying next key: {key}, Error: {e}")
    raise ValueError("No valid key found for decryption.")

def pretty_print_json(data):
    if isinstance(data, dict):
        return "\n".join([f"🔑 {k.lower()}: {v}" for k, v in data.items()])
    elif isinstance(data, list):
        return "- [" + ", ".join(map(str, data)) + "]"
    return str(data)

def execute(sender_id, message_text):
    # Extract encrypted input
    parts = message_text.split(' ', 1)
    if len(parts) < 2:
        send_message(sender_id, {"text": "❌ Error: No encrypted content provided. Use 'sks {input_encrypted}'."})
        return
    
    input_encrypted = parts[1]
    send_message(sender_id, {"text": "⏳ Processing your decryption request, please wait..."})

    try:
        config_data = json.loads(input_encrypted)
        decrypted_content = decrypt_data(config_data['d'], config_data['v'])
        
        # Format the response
        response_text = f"🎉 Decrypted Content:\n{pretty_print_json(json.loads(decrypted_content)).strip()}"
        
        # Send the response text
        send_message(sender_id, {"text": response_text})

        # Create a temporary file with the decrypted content
        temp_file_path = os.path.join(os.path.dirname(__file__), "sks_decrypted_result.txt")
        with open(temp_file_path, 'w', encoding="utf-8") as file:
            file.write(response_text)
        
        # Send the file as an attachment
        with open(temp_file_path, 'rb') as file:
            send_message(sender_id, {
                "attachment": {
                    "type": "file",
                    "payload": {
                        "is_reusable": True
                    }
                },
                "filedata": {
                    "filename": "sks_decrypted_result.txt",
                    "content": file.read(),
                    "content_type": "text/plain"
                }
            })
        
        # Clean up the temporary file
        os.remove(temp_file_path)

    except Exception as error:
        print(f"Error in execute function for {name}: {error}")
        send_message(sender_id, {"text": f"An error occurred during decryption: {error}"})
