import requests
import hashlib

vendor_token = '632b3978223b2045410032'
private_token = '632b397825523609038402'

BaseUrl = 'https://homologation.lydia-app.com'

def generate_lydia_signature(data, private_token):
    data1 = {key: value for key, value in data.items() if key != 'signature'}
    #print(f"data without signature : {data1}")
    sorted_data = sorted(data1.items())
    signature_string = "&".join([f"{key}={value}" for key, value in sorted_data])
    
    signature_string += f"&private_token={private_token}"
    print(f"signature string : {signature_string}")
    md5_hash = hashlib.md5(signature_string.encode()).hexdigest()
    return md5_hash

url = "https://homologation.lydia-app.com//api/request/state.json"
id = "12097987"

data = {
    "request_id": id,
    "vendor_token": vendor_token,
}

# Make the request with form data
response = requests.post(url, data=data)
rdict = response.json()
data_sig = {
    "amount" :0.53,
    "request_id" :id,
}


my_sig = generate_lydia_signature(data, private_token)

#print("Request Headers:", response.request.headers)
#print("Request Body:", response.request.body)

print(f"my sig : {my_sig}")
print(response.json())



