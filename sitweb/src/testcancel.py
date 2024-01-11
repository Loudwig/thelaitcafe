import requests
id = '12098154'
cancel_url = "https://homologation.lydia-app.com//api/request/cancel.json"
vendortoken = '632b3978223b2045410032'
data1 = {
    "request_id" : id,
    "vendor_token" : vendortoken 
}
cancel = requests.post(url = cancel_url, data =data1 )


print(cancel.json())