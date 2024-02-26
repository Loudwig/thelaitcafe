import requests

url = 'https://homologation.lydia-app.com/api/user/isregister.json'

data = { "data" : "e0537a2f07b16c79fe47849e10c609a34768e1d6" }

response = requests.get(url,headers=data)
if response.status_code == 200 : 
    havelydia = response.text
    print(havelydia)
else : 
    print(response.status_code)
    print(response)


