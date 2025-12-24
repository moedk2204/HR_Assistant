import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv("OLLAMA_API_KEY")
print(f"API Key: {api_key}")
print(f"API Key length: {len(api_key) if api_key else 0}")

# Test with the exact same setup
url = "https://ollama.com/api/chat"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
data = {
    "model": "gpt-oss:120b",
    "messages": [{"role": "user", "content": "Hello"}],
    "stream": False
}

try:
    response = requests.post(url, headers=headers, json=data, timeout=30)
    print(f"Status: {response.status_code}")
    if response.status_code == 401:
        print("❌ API Key is INVALID or EXPIRED")
        print(f"Response: {response.text}")
    else:
        print(f"✅ API Key works!")
        print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")