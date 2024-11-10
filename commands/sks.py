import json
from hashlib import md5
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from api.sendMessage import send_message  # Assuming send_message is available for sending responses

name = "sks"
description = "Decrypts the provided encrypted content using predefined keys."
admin_bot = True

config_keys = [
    # List of keys from the original `sks.js`
    "162exe235948e37ws6d057d9d85324e2",
    "dyv35182!",
    "dyv35224nossas!!",
    # (and so on for all keys in the provided configKeys list)
    "zbNkuNCGSLivpEuep3BcNA==",
    "175exe867948e37wb9d057d4k45604l0"
]

def aes_decrypt(data, key, iv):
    aes = AES.new(b64decode(key), AES.MODE_CBC, b64decode(iv))
    decrypted_data = aes.decrypt(b64decode(data))
    return decrypted_data.decode('utf-8').strip()

def md5_crypt(data):
    return md5(data.encode()).hexdigest()

def decrypt_data(data, version):
    for key in config_keys:
        try:
            combined_key = md5_crypt(f"{key} {version}")
            decrypted_data = aes_decrypt(data.split(".")[0], b64encode(combined_key.encode()).decode('utf-8'), data.split(".")[1])
            return decrypted_data
        except Exception as e:
            print(f"Trying next key due to error: {e}")
    raise ValueError("No valid key found for decryption.")

def pretty_print_json(data):
    result = ""
    if isinstance(data, list):
        result += f"- [{', '.join(data)}]\n"
    elif isinstance(data, dict):
        for key, value in data.items():
            if key == "message":
                continue
            if isinstance(value, (dict, list)):
                result += f"🔑 {key.lower()}:\n{pretty_print_json(value)}"
            else:
                result += f"🔑 {key.lower()}: {value}\n"
    else:
        result += str(data)
    return result.strip()

def execute(sender_id, message_text):
    input_encrypted = message_text.split(" ")[1] if len(message_text.split(" ")) > 1 else None
    
    if not input_encrypted:
        send_message(sender_id, {"text": "❌ Error: No encrypted content provided. Please use the command in the format 'sks {input_encrypted}'."})
        return

    send_message(sender_id, {"text": "⏳ Processing your decryption request, please wait..."})
    
    try:
        config_data = json.loads(input_encrypted)
        decrypted_data = decrypt_data(config_data["d"], config_data["v"])
        response_text = f"🎉 Decrypted Content:\n{pretty_print_json(json.loads(decrypted_data))}"

        # Send the decrypted result
        send_message(sender_id, {"text": response_text})
        
    except Exception as error:
        send_message(sender_id, {"text": f"An error occurred during decryption: {str(error)}"})
