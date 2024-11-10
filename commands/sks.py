from api.sendMessage import send_message
from Crypto.Cipher import AES
from Crypto.Hash import MD5
import base64
import json

name = "sks"
description = "Decrypts provided encrypted content."
admin_bot = True  # Admin-only command

# List of configuration keys as in the original JavaScript file
config_keys = [
    "162exe235948e37ws6d057d9d85324e2", "dyv35182!", "dyv35224nossas!!",
    "662ede816988e58fb6d057d9d85605e0", "962exe865948e37ws6d057d4d85604e0",
    "175exe868648e37wb9x157d4l45604l0", "c7-YOcjyk1k", "Wasjdeijs@/ÇPãoOf231#$%¨&*()_qqu&iJo>ç",
    "Ed\x01", "fubvx788b46v", "fubgf777gf6", "cinbdf665$4", "furious0982", "error", "Jicv",
    "mtscrypt", "62756C6F6B", "rdovx202b46v", "xcode788b46z", "y$I@no5#lKuR7ZH#eAgORu6QnAF*vP0^JOTyB1ZQ&*w^RqpGkY",
    "kt", "fubvx788B4mev", "thirdy1996624", "bKps&92&", "waiting", "gggggg", "fuMnrztkzbQ",
    "A^ST^f6ASG6AS5asd", "cnt", "chaveKey", "Version6", "trfre699g79r",
    "chanika acid, gimsara htpcag!!", "xcode788b46z", "cigfhfghdf665557",
    "0x0", "2$dOxdIb6hUpzb*Y@B0Nj!T!E2A6DOLlwQQhs4RO6QpuZVfjGx", "W0RFRkFVTFRd", "Bgw34Nmk",
    "B1m93p$$9pZcL9yBs0b$jJwtPM5VG@Vg", "fubvx788b46vcatsn", "$$$@mfube11!!_$$))012b4u",
    "zbNkuNCGSLivpEuep3BcNA==", "175exe867948e37wb9d057d4k45604l0"
]

def md5_hash(data):
    return MD5.new(data.encode()).digest()

def aes_decrypt(data, key, iv):
    aes_cipher = AES.new(base64.b64decode(key), AES.MODE_CBC, base64.b64decode(iv))
    decrypted_data = aes_cipher.decrypt(base64.b64decode(data))
    return decrypted_data.decode('utf-8').rstrip()

def decrypt_data(data, version):
    for key in config_keys:
        try:
            aes_key = base64.b64encode(md5_hash(key + " " + version)).decode('utf-8')
            iv = data.split(".")[1]
            decrypted_content = aes_decrypt(data.split(".")[0], aes_key, iv)
            return decrypted_content, key
        except Exception as e:
            print(f"Trying next key: {key}")
    raise ValueError("No valid key found for decryption.")

def execute(sender_id, message_text):
    # Check if the user provided encrypted content
    if not message_text:
        send_message(sender_id, {"text": "Please provide the encrypted content."})
        return

    try:
        # Assume message_text is in JSON format with fields `d` for data and `v` for version
        encrypted_input = json.loads(message_text)
        data, version = encrypted_input.get("d"), encrypted_input.get("v")

        if not data or not version:
            send_message(sender_id, {"text": "Invalid input format. Provide both encrypted content and version."})
            return

        # Attempt decryption
        decrypted_data, used_key = decrypt_data(data, version)
        send_message(sender_id, {"text": f"Successfully decrypted using key: {used_key}\n\nDecrypted Data:\n{decrypted_data}"})

    except ValueError as e:
        send_message(sender_id, {"text": f"Decryption failed: {str(e)}"})
    except Exception as e:
        send_message(sender_id, {"text": f"An error occurred: {str(e)}"})
