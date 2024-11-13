import requests

def download_file_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content.decode('utf-8')
    except requests.RequestException as e:
        print(f"Failed to download file content: {e}")
        return None
