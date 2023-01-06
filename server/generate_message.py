import rsa
import requests
from base64 import b64encode

request_url = "http://localhost:5000/reading/new"

key_file = open("public.pem", "rb")
key_data = key_file.read()
public_key = rsa.PublicKey.load_pkcs1(key_data)
message = "hello world".encode("utf8")
encrypted_message = rsa.encrypt(message, public_key)
data = b64encode(encrypted_message).decode()

params = {"data": data}
r = requests.put(url = request_url, data=params)
data = r.json()

print(data)