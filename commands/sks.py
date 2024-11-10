import os
import json
import requests
from hashlib import md5
from Crypto.Cipher import AES
from api.sendMessage import send_message  # Ensure sendMessage.py is set up as per your environment.

name = "sks"
description = "Decrypts the provided encrypted content using predefined keys."
admin_bot = True  # Adjust if only admins should use it

config_keys = [
    "162exe235948e37ws6d057d9d85324e2",
    "dyv35182!",
    "dyv35224nossas!!",
    "662ede816988e58fb6d057d9d85605e0",
    "962exe865948e37ws6d057d4d85604e0",
    "175exe868648e37wb9x157d4l45604l0",
    "c7-YOcjyk1k",
    "Wasjdeijs@/ÇPãoOf231#$%¨&*()_qqu&iJo>ç",
    "Ed\x01",
    "fubvx788b46v",
    "fubgf777gf6",
    "cinbdf665$4",
    "furious0982",
    "error",
    "Jicv",
    "mtscrypt",
    "62756C6F6B",
    "rdovx202b46v",
    "xcode788b46z",
    "y$I@no5#lKuR7ZH#eAgORu6QnAF*vP0^JOTyB1ZQ&*w^RqpGkY",
    "kt",
    "fubvx788B4mev",
    "thirdy1996624",
    "bKps&92&",
    "waiting",
    "gggggg",
    "fuMnrztkzbQ",
    "A^ST^f6ASG6AS5asd",
    "cnt",
    "chaveKey",
    "Version6",
    "trfre699g79r",
    "chanika acid, gimsara htpcag!!",
    "xcode788b46z",
    "cigfhfghdf665557",
    "0x0",
    "2$dOxdIb6hUpzb*Y@B0Nj!T!E2A6DOLlwQQhs4RO6QpuZVfjGx",
    "W0RFRkFVTFRd",
    "Bgw34Nmk",
    "B1m93p$$9pZcL9yBs0b$jJwtPM5VG@Vg",
    "fubvx788b46vcatsn",
    "$$$@mfube11!!_$$))012b4u",
    "zbNkuNCGSLivpEuep3BcNA==",
    "175exe867948e37wb9d057d4k45604l0"
]

def md5crypt(data):
    return md5(data.encode()).hexdigest()

def decrypt_data(data, version):
    for key in config_keys:
        try:
            key_hashed = md5crypt(key + " " + version).encode("utf-8")
            cipher = AES.new(key_hashed, AES.MODE_CBC, iv=key_hashed[:16])
            decrypted_data = cipher.decrypt(data).decode("utf-8")
            return json.loads(decrypted_data.strip())  # Return decrypted JSON data
        except Exception as e:
            continue
    raise ValueError("No valid decryption key found.")

async def execute(sender_id, message_text):
    # Expecting input in format: sks {encrypted_payload}
    input_data = message_text.split(' ')[1] if len(message_text.split(' ')) > 1 else None
    if not input_data:
        await send_message(sender_id, {"text": "❌ Error: No encrypted content provided. Please use the format: sks {input_encrypted}."})
        return

    await send_message(sender_id, {"text": "⏳ Processing decryption request..."})

    try:
        encrypted_data = json.loads(input_data)
        decrypted_content = decrypt_data(bytes.fromhex(encrypted_data['d']), str(encrypted_data['v']))
        decrypted_text = json.dumps(decrypted_content, indent=2)
        
        # Respond with decrypted data as text
        await send_message(sender_id, {"text": f"🎉 Decrypted Content:\n{decrypted_text}"})

    except Exception as error:
        await send_message(sender_id, {"text": f"An error occurred: {str(error)}"})
