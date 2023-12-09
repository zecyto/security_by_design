import requests
import secrets
from hashlib import sha256
import hmac

header = {'Content-type': 'application/json', 'Authorization':'Bearer axsGqZTjZtwoTnxxPINHqTLWuFNnEL'}
url = "https://smartmeter.mwoelke.de/api/customers"
response = requests.get(url=url, headers=header)
print(response.status_code)
print(response.json()[0]["smartmeters"])

original_string = "your string here"
capitalized_string = original_string.capitalize()

def generate_mac(message):
    hash_function = sha256
    key = b'\xc1C-N\xe0K\x85H^\xa1;\xc7\xdcY|\x1a'
    message_bytes = bytes(message, 'utf-8') if isinstance(message, str) else message

    mac = hmac.new(key, message_bytes, hash_function)

    return mac.hexdigest()

message = 'admin@admin'.encode() + 'user'.encode() + 'test@test'.encode() + '1702162529.3351912'.encode()

print(generate_mac(message))