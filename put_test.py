import requests

url = "http://localhost:8000/empresa/1/endpoint-productos"
payload = {
    "endpoint_productos": "https://api.escuelajs.co/api/v1/products"
}
headers = {"Content-Type": "application/json"}

response = requests.put(url, json=payload, headers=headers)
print(response.status_code)
print(response.json())
