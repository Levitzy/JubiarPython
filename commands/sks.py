import os
import json
from api.sendMessage import send_message
from Crypto.Cipher import AES
from hashlib import md5

name = "sks"
description = "Decrypts the provided encrypted content using predefined keys."
admin_bot = True

# Full list of decryption keys
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

def aes_decrypt(data, key, iv):
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(data)
        return decrypted_data.decode('utf-8').strip()
    except Exception as e:
        print(f"Decryption error with key: {key} -> {str(e)}")
        return None

def md5_crypt(data):
    return md5(data.encode('utf-8')).hexdigest()

def decrypt_data(encrypted_data, version):
    data_part, iv_part = encrypted_data.split(".")
    iv = bytes.fromhex(iv_part)
    
    for key in config_keys:
        try:
            key_md5 = md5_crypt(f"{key} {version}")
            decrypted_data = aes_decrypt(bytes.fromhex(data_part), key_md5, iv)
            if decrypted_data:
                return decrypted_data
        except Exception as e:
            print(f"Error with key {key}: {str(e)}")
    return None

def pretty_print_json(data):
    result = ''
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                result += f"🔑 {key}:\n{pretty_print_json(value)}\n"
            else:
                result += f"🔑 {key}: {value}\n"
    elif isinstance(data, list):
        result = ', '.join(map(str, data))
    else:
        result = str(data)
    return result

def execute(sender_id, message_text):
    input_encrypted = message_text.split(' ')[1] if len(message_text.split(' ')) > 1 else None

    if not input_encrypted:
        send_message(sender_id, {"text": "❌ Error: No encrypted content provided. Use format 'sks {input_encrypted}'."})
        return

    send_message(sender_id, {"text": "⏳ Processing decryption request, please wait..."})

    try:
        config_data = json.loads(input_encrypted)
        decrypted_data = decrypt_data(config_data['d'], config_data['v'])
        
        if decrypted_data:
            response_text = f"🎉 Decrypted Content:\n{pretty_print_json(json.loads(decrypted_data)).strip()}"
            send_message(sender_id, {"text": response_text})
        else:
            send_message(sender_id, {"text": "❌ Error: Decryption failed. No valid key found."})

    except Exception as e:
        send_message(sender_id, {"text": f"An error occurred during decryption: {str(e)}"})
