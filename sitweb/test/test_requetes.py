import requests
import hashlib

vendor_token = '632b3978223b2045410032'
private_token = '632b397825523609038402'

BaseUrl = 'https://homologation.lydia-app.com'

DEBUG = True

def generate_lydia_signature(data, private_token):
    data1 = {key: value for key, value in data.items() if key != 'sig'}
    print(data1)
    sorted_data = sorted(data1.items())
    signature_string = "&".join([f"{key}={value}" for key, value in sorted_data])
    signature_string += f"&private_token={private_token}"
    md5_hash = hashlib.md5(signature_string.encode()).hexdigest()
    return md5_hash

url = "https://homologation.lydia-app.com/api/request/do.json"
confirm_url = 'https://floppy-baboons-taste.loca.lt/boutique/confirm_url'

data = {
    "amount": "0.53",
    "payment_method": "auto",
    "vendor_token": vendor_token,
    "recipient": "+33600000005",
    "currency": "EUR",
    "type": "phone",
    "confirm_url" : confirm_url
}

# Make the request with form data
response = requests.post(url, data=data)


if DEBUG : 
    print("Request Headers:", response.request.headers)
    print("Request Body:", response.request.body)
    print("Response:", response.json())


