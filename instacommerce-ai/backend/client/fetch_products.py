import requests

def fetch_products(endpoint_url: str = "https://api.escuelajs.co/api/v1/products"):
    try:
        response = requests.get(endpoint_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error al obtener productos del endpoint: {str(e)}")
        return []
