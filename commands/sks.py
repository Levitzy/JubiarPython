import json
import base64
import hashlib
from Crypto.Cipher import AES
from api.sendMessage import send_message

name = "sks"
description = "Decrypts the provided content using specific configuration keys."
admin_bot = True  # Set to True for admin-only access

# Configuration keys
config_keys = [
    "162exe235948e37ws6d057d9d85324e2", "dyv35182!", "dyv35224nossas!!", 
    "662ede816988e58fb6d057d9d85605e0", "962exe865948e37ws6d057d4d85604e0",
    "175exe868648e37wb9x157d4l45604l0", "c7-YOcjyk1k", "Wasjdeijs@/ÇPãoOf231#$%¨&*()_qqu&iJo>ç",
    "Ed\x01", "fubvx788b46v", "fubgf777gf6", "cinbdf665$4", "furious0982", "error",
    "Jicv", "mtscrypt", "62756C6F6B", "rdovx202b46v", "xcode788b46z", 
    "y$I@no5#lKuR7ZH#eAgORu6QnAF*vP0^JOTyB1ZQ&*w^RqpGkY", "kt", "fubvx788B4mev", 
    "thirdy1996624", "bKps&92&", "waiting", "gggggg", "fuMnrztkzbQ", 
    "A^ST^f6ASG6AS5asd", "cnt", "chaveKey", "Version6", "trfre699g79r", 
    "chanika acid, gimsara htpcag!!", "xcode788b46z", "cigfhfghdf665557", 
    "0x0", "2$dOxdIb6hUpzb*Y@B0Nj!T!E2A6DOLlwQQhs4RO6QpuZVfjGx", "W0RFRkFVTFRd", 
    "Bgw34Nmk", "B1m93p$$9pZcL9yBs0b$jJwtPM5VG@Vg", "fubvx788b46vcatsn", 
    "$$$@mfube11!!_$$))012b4u", "zbNkuNCGSLivpEuep3BcNA==", "175exe867948e37wb9d057d4k45604l0"
]

def md5crypt(data):
    return hashlib.md5(data.encode()).hexdigest()

def aes_decrypt(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(base64.b64decode(data))
    return decrypted.decode('utf-8').rstrip('\0')

def decrypt_data(data, version):
    encrypted_content, iv = data.split('.')
    for key in config_keys:
        try:
            md5_key = md5crypt(f"{key} {version}")
            aes_key = base64.b64decode(md5_key)[:32]
            decrypted_data = aes_decrypt(encrypted_content, aes_key, base64.b64decode(iv))
            return decrypted_data, key
        except Exception as e:
            continue
    return None, None

def execute(sender_id, message_text):
    # Ensure the input format is correct
    if not message_text:
        send_message(sender_id, {"text": "❌ Error: No encrypted content provided. Usage: sks {input_encrypted_content}"})
        return

    # Parse input for encrypted content and version
    try:
        data = message_text.split()[1]
    except IndexError:
        send_message(sender_id, {"text": "❌ Error: No valid encrypted content detected. Usage: sks {input_encrypted_content}"})
        return

    version = "your_version_here"  # Replace with appropriate version if known

    # Perform decryption
    decrypted_data, successful_key = decrypt_data(data, version)
    if decrypted_data:
        send_message(sender_id, {"text": f"✅ Successfully Decrypted Content:\n\n{decrypted_data}"})
    else:
        send_message(sender_id, {"text": "❌ Error: Decryption failed. No valid key found for the provided content."})
