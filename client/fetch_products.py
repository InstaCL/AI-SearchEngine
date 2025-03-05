import requests
import os
from config.settings import PRODUCTS_API_URL

def fetch_products():
    """
    Obtiene la lista de productos desde la API definida en PRODUCTS_API_URL.
    """
    try:
        response = requests.get(PRODUCTS_API_URL)
        response.raise_for_status()  # Lanza un error si la solicitud falla
        data = response.json()  # Convertir la respuesta a JSON
        return data  # Retornar la lista de productos
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al obtener productos: {e}")
        return []
