import requests

def call_api(url, string_param, list_param):
    payload = {
        'query': string_param,
        'conversation': list_param
    }
    response = requests.request("POST", url, json=payload)
    
    # Process the response here
    # ...
    
    return response  # Assuming the API returns JSON data

# Example usage
api_url = 'http://localhost:5000/api/RAGmodel'
string_param = ""
list_param = []

while True:
    string_param = input("Question: ")

    if string_param == 'exit':
        break

    response_data = call_api(api_url, string_param, list_param)

    answer = response_data.json()

    list_param.append(string_param)
    list_param.append(answer["choices"][0]['message']['content'])

    print(answer["choices"][0]['message']['content'])