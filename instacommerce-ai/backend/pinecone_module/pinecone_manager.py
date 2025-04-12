from typing import List
from pinecone import Pinecone
import os
from openai import OpenAI
from database.models import Empresa
from database.database import SessionLocal
from config import settings

def insert_or_update_product(
    index_name: str,
    product_id: int,
    product_name: str,
    description: str,
    slug: str,
    price: float,
    category_name: str,
    category_slug: str,
    image: str,
    empresa_id: int,
):
    # Validación de claves
    if not settings.OPENAI_API_KEY or not settings.PINECONE_API_KEY:
        print("❌ Faltan claves de API")
        return False

    # 🧠 Inicializar cliente OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    texto_para_embedding = description  # 🧠 Ya viene preprocesado con los atributos seleccionados

    try:
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input=texto_para_embedding
        )
        embedding_vector = response.data[0].embedding
    except Exception as e:
        print("❌ Error generando embedding:", e)
        return False

    # 📡 Inicializar cliente Pinecone
    try:
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        index = pc.Index(index_name)
    except Exception as e:
        print("❌ Error conectando a Pinecone:", e)
        return False

    # 🔁 Insertar o actualizar el vector
    try:
        index.upsert(
            vectors=[
                {
                    "id": str(product_id),
                    "values": embedding_vector,
                    "metadata": {
                        "title": product_name,
                        "description": description,
                        "slug": slug,
                        "price": price,
                        "category": category_name,
                        "category_slug": category_slug,
                        "image": image,
                        "empresa_id": empresa_id
                    }
                }
            ],
            namespace=str(empresa_id)
        )
        print(f"✅ Producto {product_id} sincronizado en índice {index_name}")
        return True
    except Exception as e:
        print("❌ Error al insertar en Pinecone:", e)
        return False


def delete_all_products_by_empresa_id(empresa_id: int, index_name: str):
    db = SessionLocal()
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa or not empresa.api_key_pinecone:
        raise ValueError("❌ Empresa o API Key no válida")

    # Inicializar cliente Pinecone
    pc = Pinecone(api_key=empresa.api_key_pinecone)
    index = pc.Index(index_name)

    # Eliminar vectores del namespace correspondiente al ID de empresa
    index.delete(delete_all=True, namespace=str(empresa_id))

    print(f"🗑️ Todos los vectores eliminados para empresa {empresa_id} del índice '{index_name}'")
    return {"message": f"✅ Productos eliminados del índice '{index_name}' correctamente"}


def buscar_productos_relacionados(mensaje_usuario: str, empresa_id: int) -> List[dict]:
    db = SessionLocal()
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa or not empresa.api_key_pinecone or not empresa.api_key_openai:
        return []

    # 🔐 Inicializar cliente Pinecone
    pc = Pinecone(api_key=empresa.api_key_pinecone)

    # 🔐 Inicializar cliente OpenAI
    client = OpenAI(api_key=empresa.api_key_openai)

    # 🧠 Obtener embedding
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=mensaje_usuario
    )
    embedding_vector = response.data[0].embedding

    # 🔍 Buscar en índice
    index = pc.Index("ai-searchengine-productos")
    resultados = index.query(
        vector=embedding_vector,
        top_k=5,
        namespace=str(empresa_id),
        include_metadata=True
    )

    productos = []
    for match in resultados.matches:
        metadata = match.metadata
        productos.append({
            "title": metadata.get("title"),
            "price": metadata.get("price"),
            "description": metadata.get("description", "")
        })

    return productos

def obtener_indices_pinecone():
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    return [index.name for index in pc.list_indexes()] 

def listar_indices_disponibles() -> list[str]:
    from config import settings
    from pinecone import Pinecone

    # Cargar la API Key desde tu configuración personalizada
    api_key = settings.PINECONE_API_KEY
    if not api_key:
        raise ValueError("❌ No se encontró la PINECONE_API_KEY en el archivo .env")

    pc = Pinecone(api_key=api_key)
    indices = pc.list_indexes()
    return [idx['name'] for idx in indices]
