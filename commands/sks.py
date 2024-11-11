from api.sendMessage import send_message
import json
import hashlib
from Crypto.Cipher import AES
from base64 import b64decode, b64encode

# Command details
name = "sks"
description = "Decrypts user-provided encrypted JSON content directly from input and sends the decrypted message."
admin_bot = False

# Configuration keys
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

# Decryption functions
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

# Execute function
def execute(sender_id, message_text):
    try:
        # Extract the encrypted content after the command prefix
        encrypted_content = message_text.split(" ", 1)[1]
        
        # Parse the encrypted content as JSON
        try:
            content_json = json.loads(encrypted_content)
            data = content_json['d']
            version = content_json['v']
            iv = data.split(".")[1]  # Assume 'iv' is part of 'd'
            encrypted_part = data.split(".")[0]
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            raise ValueError("Invalid input format. Please provide JSON formatted as {\"v\":<version>, \"d\":\"<encrypted_part>.<iv>.<extra>\"}.")

        # Decrypt the data
        decrypted_data = decrypt_data(encrypted_part, iv, version)
        
        # Parse as JSON after cleaning
        json_data = json.loads(decrypted_data)
        
        # Format output
        formatted_output = ["🎉 Decrypted Content:"]
        formatted_output.extend(format_output(json_data))
        formatted_output_text = "\n".join(formatted_output)

        # Send message
        send_message(sender_id, {"text": formatted_output_text})
    
    except Exception as e:
        error_message = f"[ERROR] An error occurred during decryption: {e}"
        send_message(sender_id, {"text": error_message})
