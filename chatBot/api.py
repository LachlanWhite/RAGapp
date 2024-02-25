from flask import Flask, request, jsonify
import os
import json
import ContentStore
import requests

app = Flask(__name__)

def debugPrint(message):
    if app.debug:
        print(message)
    return message

@app.route('/api/ping', methods = ['GET'])
def ping():
    return debugPrint(json.dumps({'success': True})), 200

@app.route('/api/RAGmodel', methods = ['POST'])
def RAG():
    ContentS = ContentStore.ContentStore()
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': os.getenv('AUTH_TOKEN')
    }

    data = request.get_json()

    if 'query' not in data or 'conversation' not in data:
        return json.dumps({'error': 'missing parameters'}), 400
    
    query = data['query']

    conversation = data['conversation']

    response = requests.request("POST", url, headers=headers, data=ContentS.getPayload(query, conversation))

    return response

#Structure: Receive STR (query), Stack of STR (Conversation). Send STR (response), stack of STR (Conversation)
    
if __name__ == "__main__":
    app.run(debug=True)