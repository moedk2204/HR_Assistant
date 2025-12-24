import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv("OLLAMA_API_KEY")
url = "https://ollama.com/api/tags"
headers = {"Authorization": f"Bearer {api_key}"}

try:
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Available models:\n{response.text}")
except Exception as e:
    print(f"Error: {e}")