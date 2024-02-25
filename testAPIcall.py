import requests

def call_api(url, string_param, list_param):
    payload = {
        'query': string_param,
        'conversation': list_param
    }
    response = requests.request("POST", url, json=payload)
    
    # Process the response here
    # ...
    
    return response.json  # Assuming the API returns JSON data

# Example usage
api_url = 'http://localhost:5000/api/RAGmodel'
string_param = 'What are the prerequisite courses to take CSS 360?'
list_param = ['apple', 'banana', 'cherry', 'orange']

response_data = call_api(api_url, string_param, list_param)

#response_data = requests.request('POST', api_url)
print(response_data)