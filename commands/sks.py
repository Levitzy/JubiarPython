import os
import json
from api.sendMessage import send_message
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib

name = "sks"
description = "Decrypts the provided encrypted content using predefined keys."
admin_bot = True  # This command requires admin privileges

# Keys from sks.js file
config_keys = [
    "162exe235948e37ws6d057d9d85324e2", "dyv35182!", "dyv35224nossas!!", 
    "662ede816988e58fb6d057d9d85605e0", "962exe865948e37ws6d057d4d85604e0", 
    "175exe868648e37wb9x157d4l45604l0", "c7-YOcjyk1k", "Wasjdeijs@/ÇPãoOf231#$%¨&*()_qqu&iJo>ç",
    "Ed\x01", "fubvx788b46v", "fubgf777gf6", "cinbdf665$4", "furious0982",
    "error", "Jicv", "mtscrypt", "62756C6F6B", "rdovx202b46v", "xcode788b46z",
    "y$I@no5#lKuR7ZH#eAgORu6QnAF*vP0^JOTyB1ZQ&*w^RqpGkY", "kt", "fubvx788B4mev", 
    "thirdy1996624", "bKps&92&", "waiting", "gggggg", "fuMnrztkzbQ", "A^ST^f6ASG6AS5asd",
    "cnt", "chaveKey", "Version6", "trfre699g79r", "chanika acid, gimsara htpcag!!", 
    "xcode788b46z", "cigfhfghdf665557", "0x0", "2$dOxdIb6hUpzb*Y@B0Nj!T!E2A6DOLlwQQhs4RO6QpuZVfjGx",
    "W0RFRkFVTFRd", "Bgw34Nmk", "B1m93p$$9pZcL9yBs0b$jJwtPM5VG@Vg", "fubvx788b46vcatsn",
    "$$$@mfube11!!_$$))012b4u", "zbNkuNCGSLivpEuep3BcNA==", "175exe867948e37wb9d057d4k45604l0"
]

def aes_decrypt(data, key, iv):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    return (decryptor.update(data) + decryptor.finalize()).decode('utf-8')

def md5crypt(data):
    return hashlib.md5(data.encode()).digest()

def decrypt_data(encrypted_data, version):
    for key in config_keys:
        try:
            md5_key = md5crypt(f"{key} {version}")
            decrypted_text = aes_decrypt(
                data=bytes.fromhex(encrypted_data.split(".")[0]), 
                key=md5_key, 
                iv=bytes.fromhex(encrypted_data.split(".")[1])
            )
            return json.loads(decrypted_text)
        except Exception as e:
            print(f"🔍 Trying Next Key: {key} | Error: {e}")
    raise ValueError("❌ No Valid Key Found For Decryption.")

def execute(sender_id, message_text):
    input_encrypted = message_text.split(' ')[1] if ' ' in message_text else None
    
    if not input_encrypted:
        send_message(sender_id, {"text": "❌ Error: No encrypted content provided. Use the command 'sks {input_encrypted}'."})
        return

    send_message(sender_id, {"text": "⏳ Processing your decryption request, please wait..."})
    
    try:
        config_data = json.loads(input_encrypted)
        decrypted_data = decrypt_data(config_data["d"], config_data["v"])
        response_text = f"🎉 Decrypted Content:\n{json.dumps(decrypted_data, indent=2)}"
        
        # Send response text as chunks if too long
        if len(response_text) > 2000:
            for chunk in split_message(response_text):
                send_message(sender_id, {"text": chunk})
        else:
            send_message(sender_id, {"text": response_text})
            
    except Exception as e:
        error_message = f"An error occurred during decryption: {str(e)}"
        send_message(sender_id, {"text": error_message})
