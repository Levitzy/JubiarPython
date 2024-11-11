import os
import json
from hashlib import md5
from Crypto.Cipher import AES
from base64 import b64decode, b64encode
from api.sendMessage import send_message, split_message

name = "sks"
description = "Decrypts the provided encrypted content using predefined keys."
admin_bot = True  # Set to True if only admins should use it

# List of keys from the provided JavaScript code
config_keys = [
    "162exe235948e37ws6d057d9d85324e2",
    "dyv35182!", "dyv35224nossas!!", "662ede816988e58fb6d057d9d85605e0",
    "962exe865948e37ws6d057d4d85604e0", "175exe868648e37wb9x157d4l45604l0",
    "c7-YOcjyk1k", "Wasjdeijs@/ÇPãoOf231#$%¨&*()_qqu&iJo>ç", "Ed\x01", "fubvx788b46v",
    "fubgf777gf6", "cinbdf665$4", "furious0982", "error", "Jicv", "mtscrypt",
    "62756C6F6B", "rdovx202b46v", "xcode788b46z", "y$I@no5#lKuR7ZH#eAgORu6QnAF*vP0^JOTyB1ZQ&*w^RqpGkY",
    "kt", "fubvx788B4mev", "thirdy1996624", "bKps&92&", "waiting", "gggggg",
    "fuMnrztkzbQ", "A^ST^f6ASG6AS5asd", "cnt", "chaveKey", "Version6", "trfre699g79r",
    "chanika acid, gimsara htpcag!!", "xcode788b46z", "cigfhfghdf665557", "0x0",
    "2$dOxdIb6hUpzb*Y@B0Nj!T!E2A6DOLlwQQhs4RO6QpuZVfjGx", "W0RFRkFVTFRd", "Bgw34Nmk",
    "B1m93p$$9pZcL9yBs0b$jJwtPM5VG@Vg", "fubvx788b46vcatsn", "$$$@mfube11!!_$$))012b4u",
    "zbNkuNCGSLivpEuep3BcNA==", "175exe867948e37wb9d057d4k45604l0"
]

def md5crypt(data):
    return md5(data.encode()).hexdigest()

def aes_decrypt(data, key, iv):
    aes_instance = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = aes_instance.decrypt(data)
    return decrypted_data.decode("utf-8")

def decrypt_data(data, version):
    for key in config_keys:
        try:
            combined_key = md5crypt(f"{key} {version}")
            decryption_key = b64decode(combined_key)[:32]  # Truncate to 32 bytes for AES-256
            iv = b64decode(data.split(".")[1])
            encrypted_data = b64decode(data.split(".")[0])
            return aes_decrypt(encrypted_data, decryption_key, iv)
        except Exception:
            continue
    raise ValueError("No valid key found for decryption.")

def execute(sender_id, message_text):
    try:
        input_encrypted = message_text.split(" ")[1]
        if not input_encrypted:
            send_message(sender_id, {"text": "❌ Error: No encrypted content provided. Use 'sks {input_encrypted}'."})
            return

        send_message(sender_id, {"text": "⏳ Processing your decryption request, please wait..."})

        config_data = json.loads(input_encrypted)
        decrypted_data = decrypt_data(config_data['d'], config_data['v'])
        response_text = f"🎉 Decrypted Content:\n{decrypted_data}"

        # Send decrypted result as text if short enough
        if len(response_text) <= 2000:
            send_message(sender_id, {"text": response_text})
        else:
            message_chunks = split_message(response_text)
            for chunk in message_chunks:
                send_message(sender_id, {"text": chunk})

        # Optionally, save to a temporary file and send as attachment
        temp_file_path = os.path.join(os.path.dirname(__file__), "sks_decrypted_result.txt")
        with open(temp_file_path, "w") as f:
            f.write(response_text)

        with open(temp_file_path, "rb") as f:
            send_message(sender_id, {
                "attachment": {"type": "file", "payload": {"is_reusable": True}},
                "filedata": {"filename": "sks_decrypted_result.txt", "content": f, "content_type": "text/plain"}
            })

        os.remove(temp_file_path)  # Clean up the temporary file

    except Exception as e:
        send_message(sender_id, {"text": f"An error occurred during decryption: {str(e)}"})
