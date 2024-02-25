from flask import Flask, request, jsonify
import os
import json
import ContentStore
import requests

app = Flask(RAGmodel)

@app.ropute('api/ping', methods = ['GET'])
def ping():
    return jsonify({OK}), 204

@app.route('api/RAGmodel', methods = ['POST'])
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
        return jsonify({'error': 'missing parameters'}), 400
    
    query = data['query']

    conversation = data['conversation']

    response = requests.request("POST", url, headers=headers, data=ContentS.getPayload(query, conversation))

#Structure: Receive STR (query), Stack of STR (Conversation). Send STR (response), stack of STR (Conversation)