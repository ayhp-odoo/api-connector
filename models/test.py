import requests

params = {
    'access_key': '062d2886e5ba140c2fb8cbd740c751de'
}

xml = """<?xml version='1.0' encoding='utf-8'?>
<a>o</a>"""

headers = {'Content-Type': 'text/xml'}

# api_result = requests.post(
#     'http://192.168.10.52:5000/api/v1/api/xml', data=xml, headers=headers)

print(type(requests.post(
    'http://192.168.10.52:5000/api/v1/api/xml', data=xml, headers=headers)))

#api_response = api_result.json()

# print(f"\n\n\n{api_response}\n\n\n")
#print(f"\n\n\n{type(api_result)}\n\n\n")
