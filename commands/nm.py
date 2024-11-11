from api.sendMessage import send_message
import json
import hashlib
from Crypto.Cipher import AES
from base64 import b64decode, b64encode

name = "sks"
description = "Decrypts the provided encrypted content using specified keys."
admin_bot = False

# Configuration keys from the provided file
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
    aes_instance = AES.new(b64decode(key), AES.MODE_CBC, b64decode(iv))
    decrypted_data = aes_instance.decrypt(b64decode(data))
    return decrypted_data.decode('utf-8').rstrip('\x10')

def md5crypt(data):
    return hashlib.md5(data.encode()).hexdigest()

def decrypt_data(data, version):
    for key in config_keys:
        try:
            aes_key = b64encode(md5crypt(key + " " + str(version)).encode()).decode()
            iv = data.split(".")[1]
            decrypted_data = aes_decrypt(data.split(".")[0], aes_key, iv)
            return decrypted_data  # Return decrypted data directly
        except Exception:
            continue
    return None  # No valid key found

def execute(sender_id, message_text):
    try:
        # Parse input as JSON
        input_data = json.loads(message_text)
        encrypted_content = input_data.get("d")
        version = input_data.get("v")

        decrypted_content = decrypt_data(encrypted_content, version)
        
        if decrypted_content:
            response_message = f"Decryption successful:\n{decrypted_content}"
        else:
            response_message = "Decryption failed: No valid key found."

        send_message(sender_id, {"text": response_message})
    except json.JSONDecodeError:
        error_message = "Invalid input format. Please provide valid JSON data."
        send_message(sender_id, {"text": error_message})
