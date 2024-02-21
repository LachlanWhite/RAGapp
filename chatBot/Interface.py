import os
import requests
import json
import ContentStore

url = "https://api.openai.com/v1/chat/completions"

query = "What prerequisite courses are required to take CSS 350?"

ContentS = ContentStore.ContentStore()

payload = json.dumps({
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "assistant",
      "content": ContentS.createPrompt(query, 0.66)
    },
    {
      "role": "user",
      "content": query
    }
  ],
  "temperature": 1,
  "top_p": 1,
  "n": 1,
  "stream": False,
  "max_tokens": 4096,
  "presence_penalty": 0,
  "frequency_penalty": 0
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': os.getenv('AUTH_TOKEN')
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)