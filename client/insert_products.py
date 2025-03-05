import sys
import os

# Asegurar que la raíz del proyecto está en sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from client.fetch_products import fetch_products
from pinecone_module.pinecone_manager import insert_product

def insert_all_products():
    """
    Obtiene todos los productos de la API y los inserta en Pinecone.
    """
    products = fetch_products()
    
    if not products:
        print("❌ No se encontraron productos para insertar en Pinecone.")
        return
    
    for product in products:
        insert_product(product["id"], product["title"], product["description"])
    
    print("✅ Todos los productos fueron insertados en Pinecone.")

if __name__ == "__main__":
    insert_all_products()
