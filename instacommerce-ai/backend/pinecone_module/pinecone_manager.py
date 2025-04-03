from typing import List
from pinecone import Pinecone
import os
from openai import OpenAI
from database.models import Empresa
from database.database import SessionLocal
from config import settings

def insert_or_update_product(**kwargs):
    print("📥 Producto insertado o actualizado (simulación)")
    return True

def delete_all_products_by_empresa_id(empresa_id: int):
    print(f"🗑️ Productos eliminados para empresa {empresa_id} (simulación)")
    return {"message": "✅ Productos eliminados correctamente"}

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
