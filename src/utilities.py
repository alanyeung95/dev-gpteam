import http.client
import json
import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') 
OPENAI_API_ENDPOINT = os.getenv('OPENAI_API_ENDPOINT') 
print(OPENAI_API_ENDPOINT)
def call_openai_api(role, prompt):
    conn = http.client.HTTPSConnection(OPENAI_API_ENDPOINT)

    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [{"role": role, "content": prompt}]
    })

    headers = {
        'Content-Type': "application/json",
        'Authorization': f"Bearer {OPENAI_API_KEY}"
    }

    conn.request("POST", "/v1/chat/completions", payload, headers)

    res = conn.getresponse()
    data = res.read()
    conn.close()

    return data.decode("utf-8")
