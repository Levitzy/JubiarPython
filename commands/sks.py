import json
import os
from hashlib import md5
from Crypto.Cipher import AES
from base64 import b64decode, b64encode
from api.sendMessage import send_message
from tempfile import NamedTemporaryFile

name = "sks"
description = "Decrypts the provided encrypted content using predefined keys."
admin_bot = True

config_keys = [
    "162exe235948e37ws6d057d9d85324e2", "dyv35182!", "dyv35224nossas!!", 
    "662ede816988e58fb6d057d9d85605e0", "962exe865948e37ws6d057d4d85604e0", 
    "175exe868648e37wb9x157d4l45604l0", "c7-YOcjyk1k", "Wasjdeijs@/ÇPãoOf231#$%¨&*()_qqu&iJo>ç"
]

def aes_decrypt(data, key, iv):
    aes_instance = AES.new(b64decode(key), AES.MODE_CBC, b64decode(iv))
    decrypted_data = aes_instance.decrypt(b64decode(data))
    return decrypted_data.decode('utf-8').strip()

def md5_crypt(data):
    return md5(data.encode()).hexdigest()

def decrypt_data(data, version):
    for key in config_keys:
        try:
            # Generate decryption key
            decryption_key = b64encode(md5_crypt(key + " " + version).encode())
            decrypted_data = aes_decrypt(data.split(".")[0], decryption_key, data.split(".")[1])
            return decrypted_data
        except Exception:
            continue  # Try next key if decryption fails
    raise ValueError("❌ No valid key found for decryption.")

def execute(sender_id, message_text):
    try:
        input_encrypted = message_text.split(" ")[1]
        if not input_encrypted:
            send_message(sender_id, {"text": "❌ Error: No encrypted content provided. Please use the command in the format 'sks {input_encrypted}'."})
            return

        send_message(sender_id, {"text": "⏳ Processing your decryption request, please wait..."})

        # Parse input as JSON and decrypt
        config_data = json.loads(input_encrypted)
        decrypted_data = decrypt_data(config_data['d'], config_data['v'])

        # Prepare decrypted content as response text
        response_text = f"🎉 Decrypted Content:\n{decrypted_data}"

        # Send decrypted result message
        send_message(sender_id, {"text": response_text})

        # Write decrypted content to a temporary file and send it as an attachment
        with NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as temp_file:
            temp_file.write(decrypted_data)
            temp_file_path = temp_file.name

        with open(temp_file_path, "rb") as file_to_send:
            send_message(sender_id, {
                "attachment": {
                    "type": "file",
                    "payload": {"is_reusable": True}
                },
                "filedata": {
                    "filename": "sks_decrypted_result.txt",
                    "content": file_to_send,
                    "content_type": "text/plain"
                }
            })

        # Clean up temporary file
        os.remove(temp_file_path)

    except Exception as e:
        send_message(sender_id, {"text": f"An error occurred during decryption: {str(e)}"})
