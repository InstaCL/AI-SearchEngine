import requests
from backend.database.models import Empresa


def fetch_products(endpoint_url: str = "https://api.escuelajs.co/api/v1/products"):
    """
    Método simple para obtener todos los productos (sin paginación).
    """
    try:
        response = requests.get(endpoint_url)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return data
        print("⚠️ La respuesta del endpoint no es una lista.")
        return []
    except Exception as e:
        print(f"❌ Error al obtener productos del endpoint: {str(e)}")
        return []


def fetch_products_paginated(endpoint_url: str, limit: int = 100):
    """
    Generator que obtiene productos paginados usando parámetros offset + limit.
    Ideal para endpoints que manejan grandes volúmenes de productos.
    """
    offset = 0
    total_recibidos = 0

    while True:
        try:
            paginated_url = f"{endpoint_url}?offset={offset}&limit={limit}"
            response = requests.get(paginated_url)
            response.raise_for_status()
            productos = response.json()

            if not productos or not isinstance(productos, list):
                print("📭 No se recibieron más productos o la respuesta no es válida.")
                break

            print(f"📦 Productos recibidos: {len(productos)} (offset: {offset})")

            for producto in productos:
                yield producto

            total_recibidos += len(productos)

            if len(productos) < limit:
                print("✅ Fin de la paginación.")
                break

            offset += limit

        except Exception as e:
            print(f"❌ Error en fetch paginado: {str(e)}")
            break


def generar_texto_producto(producto: dict, empresa: Empresa) -> str:
    """
    Construye el texto que será embebido en Pinecone,
    usando solo los atributos seleccionados por la empresa.
    """
    atributos = empresa.get_atributos_sincronizados()
    if not atributos:
        print(f"⚠️ Empresa {empresa.id} no tiene atributos seleccionados.")
        return ""

    texto = " ".join(str(producto.get(attr, "")) for attr in atributos)
    return texto.strip()
