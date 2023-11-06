import http.client
import json

def call_openai_api(prompt):
    conn = http.client.HTTPSConnection("api.openai.com")

    api_key = "your-api-key"  # Make sure to keep your API keys secure
    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    })

    headers = {
        'Content-Type': "application/json",
        'Authorization': f"Bearer {api_key}"
    }

    conn.request("POST", "/v1/chat/completions", payload, headers)

    res = conn.getresponse()
    data = res.read()
    conn.close()

    return data.decode("utf-8")
