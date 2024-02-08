import requests
import os

url_login = 'http://127.0.0.1:8000/api/login'
url_transaction = 'http://127.0.0.1:8000/api/getTransaction'
url_update = 'http://127.0.0.1:8000/api/update'

try:
    username = os.environ["USERNAME"]
except KeyError as e:
    raise RuntimeError("Could not find a USERNAME in environment") from e
try:
    password = os.environ["PASSWORD"]
except KeyError as e1:
    raise RuntimeError("Could not find a PASSWORD in environment") from e1

def api_connect():
    s = requests.Session() #
    response = s.post(url_login,data={ "username" : username, "password" : password})

    if response.status_code == 200: 
        # ici connecter to the API
        data = response.json()
        print(data)
    else : 
        print(response.status_code)
        print(response.json())
    s.close()


api_connect()



# data = {
#     'request_id' : '12098145'
# }

#url1 = 'http://127.0.0.1:8000/boutique/api/update'

# response1 = s.post(url1, headers=headers,json=data)

# if response1.status_code == 200: 
#     data = response1.json()
#     print(data)
# else : 
#     print(response1.status_code)
#     print(response1)