from typing import List
import pinecone
import os
from openai import OpenAI
from database.models import Empresa
from database.database import SessionLocal

def insert_or_update_product(**kwargs):
    print("📥 Producto insertado o actualizado (simulación)")
    return True

def delete_all_products_by_empresa_id(empresa_id: int):
    print(f"🗑️ Productos eliminados para empresa {empresa_id} (simulación)")
    return {"message": "✅ Productos eliminados correctamente"}

def buscar_productos_relacionados(mensaje_usuario: str, empresa_id: int) -> List[dict]:
    # Carga la API key desde la BD
    db = SessionLocal()
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa or not empresa.api_key_pinecone or not empresa.api_key_openai:
        return []

    # Set API keys
    pinecone.init(api_key=empresa.api_key_pinecone, environment="gcp-starter")  # Reemplaza si es otro env
    client = OpenAI(api_key=empresa.api_key_openai)

    # Embedding del mensaje
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=mensaje_usuario
    )
    embedding_vector = response.data[0].embedding

    # Buscar en el índice
    index = pinecone.Index("ai-searchengine-productos")
    resultados = index.query(vector=embedding_vector, top_k=5, namespace=str(empresa_id), include_metadata=True)

    productos = []
    for match in resultados.matches:
        metadata = match.metadata
        productos.append({
            "title": metadata.get("title"),
            "price": metadata.get("price"),
            "description": metadata.get("description", "")
        })

    return productos
