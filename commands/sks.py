from api.sendMessage import send_message
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from hashlib import md5
import json
import os

name = "sks"
description = "Decrypts the provided encrypted content using predefined keys and sends the decrypted content as a file."
admin_bot = True

# Define your encryption keys as in sks.js
config_keys = [
    "162exe235948e37ws6d057d9d85324e2",
    "dyv35182!",
    "dyv35224nossas!!",
    "662ede816988e58fb6d057d9d85605e0",
    "962exe865948e37ws6d057d4d85604e0",
    # add the rest of the keys here...
]

def aes_decrypt(data, key, iv):
    decryptor = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    ).decryptor()
    decrypted_data = decryptor.update(data) + decryptor.finalize()
    return decrypted_data.decode("utf-8")

def md5crypt(data):
    return md5(data.encode()).digest()

def decrypt_data(data, version):
    for key in config_keys:
        try:
            key_bytes = md5crypt(key + " " + version)
            iv, encrypted_data = data.split(".")[1], data.split(".")[0]
            decrypted_data = aes_decrypt(
                bytes.fromhex(encrypted_data),
                key_bytes,
                bytes.fromhex(iv)
            )
            return decrypted_data
        except Exception:
            continue
    raise ValueError("No Valid Key Found For Decryption")

def execute(sender_id, message_text):
    input_encrypted = message_text.split(' ')[1] if len(message_text.split(' ')) > 1 else None

    if not input_encrypted:
        send_message(sender_id, {"text": "❌ Error: No encrypted content provided. Please use the command in the format 'sks {input_encrypted}'."})
        return

    send_message(sender_id, {"text": "⏳ Processing your decryption request, please wait..."})

    try:
        config_data = json.loads(input_encrypted)
        decrypted_data = decrypt_data(config_data['d'], config_data['v'])

        # Formatting the response
        response_text = f"🎉 Decrypted Content:\n{decrypted_data}"
        send_message(sender_id, {"text": response_text})

        # Write decrypted result to a file
        temp_file_path = os.path.join(os.path.dirname(__file__), "sks_decrypted_result.txt")
        with open(temp_file_path, "w", encoding="utf-8") as file:
            file.write(decrypted_data)

        # Send the file to the user
        send_message(sender_id, {
            "attachment": {
                "type": "file",
                "payload": {
                    "is_reusable": True
                }
            },
            "filedata": {
                "filename": "sks_decrypted_result.txt",
                "content": open(temp_file_path, "rb").read(),
                "content_type": "text/plain"
            }
        })

        # Clean up the file after sending
        os.remove(temp_file_path)
    except Exception as error:
        print(f"Error executing {name} command:", error)
        send_message(sender_id, {"text": f"An error occurred during decryption: {error}"})
