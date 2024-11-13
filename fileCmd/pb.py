from api.sendMessage import send_message
from api.downloadFile import download_file_content
import base64
import re
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def b64decode(content):
    """Decode Base64 content."""
    return base64.b64decode(content)

def pbkdf2_key_gen(password, salt, count=1000, dk_len=16):
    """Generate a PBKDF2 key with the specified parameters."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=dk_len,
        salt=salt,
        iterations=count,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def aes_decrypt(ciphertext, key, nonce):
    """Perform AES-GCM decryption."""
    aesgcm = AESGCM(key)
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext
    except Exception as e:
        print("Decryption failed:", e)
        return None

def remove_padding(decrypted_text):
    """Remove padding from decrypted text."""
    pad_len = decrypted_text[-1]
    return decrypted_text[:-pad_len]

def decrypt(encrypted_content):
    """Decrypt encrypted content formatted as salt.nonce.ciphertext."""
    arr_content = encrypted_content.split(".")
    salt = b64decode(arr_content[0].strip())
    nonce = b64decode(arr_content[1].strip())
    cipher = b64decode(arr_content[2].strip())

    config_enc_password = "Cw1G6s0K8fJVKZmhSLZLw3L1R3ncNJ2e"
    pbkdf2_key = pbkdf2_key_gen(config_enc_password, salt)
    decrypted_data = aes_decrypt(cipher, pbkdf2_key, nonce)

    if decrypted_data is None:
        return "Failed to decrypt AES."

    decrypted_data = remove_padding(decrypted_data).decode('utf-8')
    pattern = re.compile(r"<entry key=\"(.*?)\">(.*?)</entry>")
    result_builder = []
    
    for match in pattern.finditer(decrypted_data):
        key, value = match.groups()
        result_builder.append(f"[ADW] [{key}]= {value}")

    result_builder.append("\n\nAnonymous Decrypting World")
    return "\n".join(result_builder)

def handle_file(sender_id, file_url):
    """Process the .pb encrypted file, decrypt content, and send message and file attachment."""
    try:
        # Download file content
        encrypted_content = download_file_content(file_url).decode("utf-8")
        
        # Decrypt the content
        decrypted_message = decrypt(encrypted_content)
        
        # Send decrypted result as a message
        send_message(sender_id, {"text": decrypted_message})

        # Save decrypted result to a file
        temp_file_path = os.path.join(os.path.dirname(__file__), "decrypted.txt")
        with open(temp_file_path, "w", encoding="utf-8") as file:
            file.write(decrypted_message)

        # Send the file attachment
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

        # Provide feedback on file size
        file_size_kb = os.path.getsize(temp_file_path) / 1024
        send_message(sender_id, {
            "text": f"Decryption complete. Attached file 'decrypted.txt' ({file_size_kb:.2f} KB) contains the detailed results."
        })

        # Clean up temporary file
        os.remove(temp_file_path)

    except Exception as e:
        send_message(sender_id, {"text": f"Error processing file: {e}"})
