from api.sendMessage import send_message
import json
from Crypto.Cipher import AES
import hashlib
import base64

name = "sks"
description = "Decrypts the provided encrypted content using predefined keys."
admin_bot = True

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
    aes_instance = AES.new(key, AES.MODE_CBC, iv)
    decrypted = aes_instance.decrypt(base64.b64decode(data))
    return decrypted.decode("utf-8").strip()

def md5crypt(data):
    return hashlib.md5(data.encode()).hexdigest()

def decrypt_data(data, version):
    for key in config_keys:
        try:
            hashed_key = md5crypt(key + " " + version)
            key_bytes = base64.b64encode(hashed_key.encode())[:32]
            iv = data.split(".")[1].encode()
            decrypted_data = aes_decrypt(data.split(".")[0], key_bytes, iv)
            return json.loads(decrypted_data)
        except Exception:
            continue
    raise ValueError("❌ No Valid Key Found For Decryption.")

def execute(sender_id, message_text):
    input_encrypted = message_text.split(' ', 1)[-1]
    
    if not input_encrypted:
        send_message(sender_id, {"text": "❌ Error: No encrypted content provided. Please use 'sks {input_encrypted}'."})
        return

    send_message(sender_id, {"text": "⏳ Processing your decryption request, please wait..."})

    try:
        config_data = json.loads(input_encrypted)
        decrypted_content = decrypt_data(config_data["d"], str(config_data["v"]))
        response_text = f"🎉 Decrypted Content:\n{json.dumps(decrypted_content, indent=2)}"
        
        # Send decrypted content as text
        send_message(sender_id, {"text": response_text})
    except Exception as e:
        send_message(sender_id, {"text": f"An error occurred during decryption: {str(e)}"})
