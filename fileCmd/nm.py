import base64
from Crypto.Cipher import AES
from api.sendMessage import send_message
import requests

# Constants
DECRYPTION_KEY = base64.b64decode("X25ldHN5bmFfbmV0bW9kXw==")  # Replace with your decryption key

def decrypt_aes_ecb_128(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted

def handle_file(sender_id, file_url):
    try:
        file_content = download_file_content(file_url)
        encrypted_content = base64.b64decode(file_content)
        decrypted_text = decrypt_aes_ecb_128(encrypted_content, DECRYPTION_KEY).rstrip(b"\x00").decode('utf-8')

        if "{" in decrypted_text and "}" in decrypted_text:
            json_data = decrypted_text[decrypted_text.find("{"):decrypted_text.rfind("}") + 1]
            send_message(sender_id, {"text": f"Decryption successful. JSON content: {json_data}"})
        else:
            send_message(sender_id, {"text": f"Decryption successful: {decrypted_text}"})

    except Exception as e:
        send_message(sender_id, {"text": f"Error during decryption: {str(e)}"})

def download_file_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Failed to download file content: {e}")
        return None
