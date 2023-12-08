import requests

header = {'Content-type': 'application/json', 'Authorization':'Bearer axsGqZTjZtwoTnxxPINHqTLWuFNnEL'}
url = "https://smartmeter.mwoelke.de/api/customers"
response = requests.get(url=url, headers=header)
print(response.status_code)
print(response.json()[0]["smartmeters"])
