import requests
import hashlib

url = "https://homologation.lydia-app.com/api/request/status.json"
vendor_token = "632b3978223b2045410032"
business_private_token = "632b397825523609038402"
id = "12097986"




def generate_lydia_signature(params):
    # Sort the params by keys
    sorted_params = sorted(params.items())

    # Create the signature string
    signature_string = "&".join([f"{key}={value}" for key, value in sorted_params])

    # Calculate the MD5 hash
    md5_hash = hashlib.md5(signature_string.encode()).hexdigest()

    return md5_hash

# Provide one of the following: request_id, request_uuid, or order_ref and vendor_token
params = {
    "request_id": id,
    "vendor_token" : vendor_token
}

# Make the request to fetch the status
response = requests.post(url, data=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Convert the JSON response to a dictionary
    response_dict = response.json()

    # Check if a signature is provided in the response
    if "signature" in response_dict:
        # Verify the signature
        signature_params = {
            "amount": response_dict.get("amount", ""),
            "request_id": response_dict.get("request_id", ""),
            # Include either "request_uuid" or "order_ref" based on what you provided
            # "request_uuid": response_dict.get("request_uuid", ""),
            # OR "order_ref": response_dict.get("order_ref", ""),
            "vendor_token": vendor_token,
            "business_private_token": business_private_token,
        }

        # Generate the signature
        calculated_signature = generate_lydia_signature(signature_params)

        # Compare the calculated signature with the one provided in the response
        if calculated_signature == response_dict["signature"]:
            print("Signature verification successful.")
        else:
            print("Signature verification failed.")
    else:
        print("No signature found in the response.")

    # Print the status response
    print(response_dict)
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)  # Print the response content for debugging purposes


