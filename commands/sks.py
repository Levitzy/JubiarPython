from api.sendMessage import send_message
from hashlib import md5
from Crypto.Cipher import AES
import base64
import json

name = "sks"
description = "Decrypts encrypted content based on input key."
admin_bot = True  # This command is for admin only

# Configuration keys as provided
config_keys = [
    "162exe235948e37ws6d057d9d85324e2", "dyv35182!", "dyv35224nossas!!",
    "662ede816988e58fb6d057d9d85605e0", "962exe865948e37ws6d057d4d85604e0",
    "175exe868648e37wb9x157d4l45604l0", "c7-YOcjyk1k",
    "Wasjdeijs@/ÇPãoOf231#$%¨&*()_qqu&iJo>ç", "Ed\x01", "fubvx788b46v",
    "fubgf777gf6", "cinbdf665$4", "furious0982", "error", "Jicv", "mtscrypt",
    "62756C6F6B", "rdovx202b46v", "xcode788b46z", "y$I@no5#lKuR7ZH#eAgORu6QnAF*vP0^JOTyB1ZQ&*w^RqpGkY",
    "kt", "fubvx788B4mev", "thirdy1996624", "bKps&92&", "waiting", "gggggg",
    "fuMnrztkzbQ", "A^ST^f6ASG6AS5asd", "cnt", "chaveKey", "Version6",
    "trfre699g79r", "chanika acid, gimsara htpcag!!", "xcode788b46z",
    "cigfhfghdf665557", "0x0", "2$dOxdIb6hUpzb*Y@B0Nj!T!E2A6DOLlwQQhs4RO6QpuZVfjGx",
    "W0RFRkFVTFRd", "Bgw34Nmk", "B1m93p$$9pZcL9yBs0b$jJwtPM5VG@Vg",
    "fubvx788b46vcatsn", "$$$@mfube11!!_$$))012b4u", "zbNkuNCGSLivpEuep3BcNA==",
    "175exe867948e37wb9d057d4k45604l0"
]

def md5crypt(data):
    return md5(data.encode()).hexdigest()

def aes_decrypt(data, key, iv):
    cipher = AES.new(base64.b64decode(key), AES.MODE_CBC, base64.b64decode(iv))
    decrypted = cipher.decrypt(base64.b64decode(data))
    return decrypted.decode('utf-8').rstrip("\0")

def decrypt_data(data, version):
    for key in config_keys:
        try:
            key_hash = md5crypt(f"{key} {version}")
            decrypted_data = aes_decrypt(data.split(".")[0], base64.b64encode(key_hash.encode()).decode(), data.split(".")[1])
            return decrypted_data, key
        except Exception:
            continue
    return None, None

def execute(sender_id, message_text):
    # Ensure input is provided
    if not message_text:
        send_message(sender_id, {"text": "Error: Please provide the encrypted content to decrypt."})
        return
    
    try:
        # Assume message_text is JSON with 'd' (data) and 'v' (version)
        input_data = json.loads(message_text)
        if 'd' not in input_data or 'v' not in input_data:
            send_message(sender_id, {"text": "Error: Missing required fields 'd' and 'v' in input."})
            return
        
        encrypted_content = input_data['d']
        version = input_data['v']
        
        decrypted_data, key_used = decrypt_data(encrypted_content, version)
        
        if decrypted_data:
            send_message(sender_id, {"text": f"✅ Successfully Decrypted Using The Key: {key_used}\n\nDecrypted Content:\n{decrypted_data}"})
        else:
            send_message(sender_id, {"text": "❌ No Valid Key Found For Decryption."})
    
    except json.JSONDecodeError:
        send_message(sender_id, {"text": "Error: Invalid JSON format. Please provide valid input."})
    except Exception as e:
        send_message(sender_id, {"text": f"[ERROR] An Error Occurred During Decryption: {str(e)}"})
