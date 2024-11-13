import base64
import json
import hashlib
from Crypto.Cipher import AES
from api.sendMessage import send_message
import os
import requests

# List of encryption keys
config_keys = [
    "162exe235948e37ws6d057d9d85324e2",
    "dyv35182!",
    "dyv35224nossas!!",
    # Add remaining keys here...
]

def aes_decrypt(data, key, iv):
    aes_instance = AES.new(base64.b64decode(key), AES.MODE_CBC, base64.b64decode(iv))
    decrypted_data = aes_instance.decrypt(base64.b64decode(data))
    return decrypted_data.decode('utf-8').rstrip('\x10')

def md5crypt(data):
    return hashlib.md5(data.encode()).digest()  # Use digest to get a 16-byte MD5 hash directly for AES

def clean_json_data(data):
    start = data.find('{')
    end = data.rfind('}') + 1
    if start == -1 or end == -1:
        raise ValueError("Failed to locate JSON data")
    return data[start:end]

def decrypt_data(data, iv, version):
    for key in config_keys:
        try:
            # Create a 16-byte AES key using MD5 digest of key + version
            aes_key = base64.b64encode(md5crypt(key + " " + str(version))).decode()
            decrypted_data = aes_decrypt(data, aes_key, iv)
            # Attempt to clean JSON data after decryption
            return clean_json_data(decrypted_data)
        except Exception as e:
            print(f"Failed to decrypt with key '{key}': {e}")  # Log each failed key attempt for debugging
            continue
    raise Exception("No valid key found")

def format_output(data):
    lines = []
    for key, value in data.items():
        if key == "message":
            continue
        if isinstance(value, dict):
            lines.append(f"🔑 {key}:")
            lines.extend(format_output(value))
        elif isinstance(value, list):
            lines.append(f"🔑 {key}: [{', '.join(map(str, value))}]")
        else:
            lines.append(f"🔑 {key}: {value}")
    return lines

def handle_file(sender_id, file_url):
    try:
        # Download the file content
        file_content = download_file_content(file_url)
        content_json = json.loads(file_content)
        data = content_json['d']
        version = content_json['v']
        iv = data.split(".")[1]
        encrypted_part = data.split(".")[0]

        decrypted_data = decrypt_data(encrypted_part, iv, version)
        json_data = json.loads(decrypted_data)

        formatted_output = ["🎉 Decrypted Content:"]
        formatted_output.extend(format_output(json_data))
        formatted_content = "\n".join(formatted_output)

        # Send decrypted content as a message
        send_message(sender_id, {"text": formatted_content})

        # Save and send the result as a document
        temp_file_path = os.path.join(os.path.dirname(__file__), "decrypted.txt")
        with open(temp_file_path, "w", encoding="utf-8") as file:
            file.write(formatted_content)

        with open(temp_file_path, "rb") as file:
            send_message(sender_id, {
                "attachment": {
                    "type": "file",
                    "payload": {}
                },
                "filedata": {
                    "filename": "decrypted.txt",
                    "content": file,
                    "content_type": "text/plain"
                }
            })

        file_size_kb = os.path.getsize(temp_file_path) / 1024
        send_message(sender_id, {
            "text": f"Decryption complete. Attached file 'decrypted.txt' ({file_size_kb:.2f} KB) contains the detailed results."
        })

        os.remove(temp_file_path)

    except Exception as e:
        error_message = f"[ERROR] An error occurred during decryption: {e}"
        send_message(sender_id, {"text": error_message})

def download_file_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content.decode('utf-8')
    except requests.RequestException as e:
        print(f"Failed to download file content: {e}")
        return None
