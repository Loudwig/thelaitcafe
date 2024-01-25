import requests

url = 'http://127.0.0.1:8000/boutique/getTransaction'
api_key = '12'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}',
}

response = requests.post(url, headers=headers)
if response.status_code == 200: 
    data = response.json()
    print(data)
else : 
    print(response.status_code)
    print(response)


data = {
    'request_id' : '12098145'
}

url1 = 'http://127.0.0.1:8000/boutique/update'
response1 = requests.post(url1, headers=headers,json=data)

if response1.status_code == 200: 
    data = response1.json()
    print(data)
else : 
    print(response1.status_code)
    print(response1)