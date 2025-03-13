# client/fetch_products.py

import requests
from config.settings import PRODUCTS_API_URL

def fetch_products():
    """
    Obtiene productos desde la API externa y filtra solo los que tienen al menos una imagen.
    """
    try:
        response = requests.get(PRODUCTS_API_URL)
        response.raise_for_status()
        productos_raw = response.json()

        productos_procesados = []
        for producto in productos_raw:
            images = producto.get("images", [])
            if not images or not isinstance(images, list) or not any(images):
                continue  # Ignorar productos sin imágenes válidas

            producto_transformado = {
                "id": producto.get("id"),
                "title": producto.get("title", ""),
                "slug": producto.get("slug", ""),
                "price": producto.get("price", 0),
                "description": producto.get("description", ""),
                "category_name": producto.get("category", {}).get("name", ""),
                "category_slug": producto.get("category", {}).get("slug", ""),
                "image": images[0]  # Tomamos solo la primera imagen
            }

            productos_procesados.append(producto_transformado)

        print(f"✅ Productos válidos procesados: {len(productos_procesados)}")
        return productos_procesados

    except Exception as e:
        print(f"❌ Error al obtener productos: {e}")
        return []
