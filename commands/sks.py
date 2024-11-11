from api.sendMessage import send_message
from Crypto.Cipher import AES
from Crypto.Hash import MD5
import base64
import json

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
    "62756C6B",
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
    aes_instance = AES.new(base64.b64decode(key), AES.MODE_CBC, base64.b64decode(iv))
    result = aes_instance.decrypt(base64.b64decode(data)).decode('utf-8')
    return result

def md5_crypt(data):
    return MD5.new(data.encode()).hexdigest()

def decrypt_data(data, version):
    for key in config_keys:
        try:
            decrypted_data = aes_decrypt(
                data.split(".")[0],
                base64.b64encode(md5_crypt(key + " " + version).encode()).decode(),
                data.split(".")[1]
            )
            return {"decrypted_data": decrypted_data}
        except Exception as e:
            # Removed print statement here
            pass  # You can add logging or other handling if needed
    raise ValueError("No valid key found for decryption.")

def pretty_print_json(data):
    result = ''
    if isinstance(data, list):
        result += f"- [{','.join(data)}]\n"
    elif isinstance(data, dict):
        for key, value in data.items():
            if key == "message":
                continue
            if isinstance(value, (dict, list)):
                result += f"🔑 {key.lower()}:\n"
                result += pretty_print_json(value)
            else:
                result += f"🔑 {key.lower()}: {value}\n"
    else:
        result += f"{data}\n"
    return result

def execute(sender_id, message_text):
    try:
        input_encrypted = message_text.split(' ')[1]
        if not input_encrypted:
            send_message(sender_id, {"text": "❌ Error: No encrypted content provided. Please use the command in the format 'sks {input_encrypted}'."})
            return

        send_message(sender_id, {"text": "⏳ Processing your decryption request, please wait..."})

        config_data = json.loads(input_encrypted)
        decrypted_data = decrypt_data(config_data.get('d'), config_data.get('v'))['decrypted_data']

        response_text = f"🎉 Decrypted Content:\n{pretty_print_json(json.loads(decrypted_data)).strip()}"

        send_message(sender_id, {"text": response_text})

    except Exception as e:
        print(f"Error executing {name} command:", e)
        send_message(sender_id, {"text": f"An error occurred during decryption: {e}"})