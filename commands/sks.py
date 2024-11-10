import os
import json
from hashlib import md5
from Crypto.Cipher import AES
from base64 import b64decode
from api.sendMessage import send_message

name = "sks"
description = "Decrypts the provided encrypted content using predefined keys."
admin_bot = True  # This command is intended for admin use only

# Define config keys
config_keys = [
    "162exe235948e37ws6d057d9d85324e2", "dyv35182!", "dyv35224nossas!!", "662ede816988e58fb6d057d9d85605e0",
    "962exe865948e37ws6d057d4d85604e0", "175exe868648e37wb9x157d4l45604l0", "c7-YOcjyk1k",
    "Wasjdeijs@/ÇPãoOf231#$%¨&*()_qqu&iJo>ç", "Ed\x01", "fubvx788b46v", "fubgf777gf6", "cinbdf665$4",
    "furious0982", "error", "Jicv", "mtscrypt", "62756C6F6B", "rdovx202b46v", "xcode788b46z",
    "y$I@no5#lKuR7ZH#eAgORu6QnAF*vP0^JOTyB1ZQ&*w^RqpGkY", "kt", "fubvx788B4mev", "thirdy1996624", 
    "bKps&92&", "waiting", "gggggg", "fuMnrztkzbQ", "A^ST^f6ASG6AS5asd", "cnt", "chaveKey",
    "Version6", "trfre699g79r", "chanika acid, gimsara htpcag!!", "xcode788b46z", "cigfhfghdf665557",
    "0x0", "2$dOxdIb6hUpzb*Y@B0Nj!T!E2A6DOLlwQQhs4RO6QpuZVfjGx", "W0RFRkFVTFRd", "Bgw34Nmk",
    "B1m93p$$9pZcL9yBs0b$jJwtPM5VG@Vg", "fubvx788b46vcatsn", "$$$@mfube11!!_$$))012b4u", 
    "zbNkuNCGSLivpEuep3BcNA==", "175exe867948e37wb9d057d4k45604l0"
]

# Helper functions for decryption and MD5 hashing
def aes_decrypt(data, key, iv):
    aes_instance = AES.new(key, AES.MODE_CBC, iv)
    decrypted = aes_instance.decrypt(data)
    return decrypted.decode('utf-8').strip()

def md5_hash(data):
    return md5(data.encode()).digest()

def decrypt_data(data, version):
    for key in config_keys:
        try:
            key_md5 = md5_hash(key + " " + version)
            iv = b64decode(data.split(".")[1])
            decrypted_data = aes_decrypt(b64decode(data.split(".")[0]), key_md5, iv)
            return decrypted_data
        except Exception as e:
            continue
    raise ValueError("No valid key found for decryption.")

def execute(sender_id, message_text):
    try:
        input_encrypted = message_text.split(' ')[1]
        if not input_encrypted:
            send_message(sender_id, {"text": "❌ Error: No encrypted content provided. Please use the command in the format 'sks {input_encrypted}'."})
            return

        send_message(sender_id, {"text": "⏳ Processing your decryption request, please wait..."})
        
        # Parse and decrypt data
        config_data = json.loads(input_encrypted)
        decrypted_data = decrypt_data(config_data["d"], config_data["v"])
        pretty_output = json.dumps(json.loads(decrypted_data), indent=2)

        # Send the decrypted content
        send_message(sender_id, {"text": f"🎉 Decrypted Content:\n{pretty_output}"})

        # Save and send as a file
        temp_file_path = "/tmp/sks_decrypted_result.txt"
        with open(temp_file_path, "w") as file:
            file.write(pretty_output)
        
        # Sending the file as an attachment
        send_message(sender_id, {
            "attachment": {
                "type": "file",
                "payload": {
                    "url": temp_file_path,
                    "is_reusable": True
                }
            }
        })
    except Exception as e:
        send_message(sender_id, {"text": f"An error occurred during decryption: {str(e)}"})
