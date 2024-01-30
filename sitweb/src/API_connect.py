import requests

url_login = 'http://127.0.0.1:8000/api/login'
url_transaction = 'http://127.0.0.1:8000/api/getTransaction'
url_update = 'http://127.0.0.1:8000/api/getTransaction'

username = "ROMAIN"
password = "ROMAIN"

def api_connect():
    s = requests.Session() # Création d'une session pour avoir être connecté en temps que superuser
    # il faut cacher les username et password.... envoyé le hash ? je sais pas trop...
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