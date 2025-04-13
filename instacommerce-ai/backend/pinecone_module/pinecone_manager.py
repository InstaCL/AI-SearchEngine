from typing import List
from pinecone import Pinecone
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
    if not settings.OPENAI_API_KEY or not settings.PINECONE_API_KEY:
        print("❌ Faltan claves de API")
        return False

    # Inicializar cliente OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    texto_para_embedding = description  # Ya viene filtrado con atributos seleccionados

    try:
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input=texto_para_embedding
        )
        embedding_vector = response.data[0].embedding
    except Exception as e:
        print(f"❌ Error generando embedding para producto {product_id}: {str(e)}")
        return False

    # Inicializar cliente Pinecone
    try:
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        index = pc.Index(index_name)
    except Exception as e:
        print(f"❌ Error conectando a Pinecone: {str(e)}")
        return False

    # Obtener atributos seleccionados de la empresa
    try:
        with SessionLocal() as db:
            empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
            atributos = empresa.get_atributos_sincronizados() if empresa else []
    except Exception as e:
        print(f"❌ Error accediendo a atributos de empresa {empresa_id}: {str(e)}")
        return False

    # Construir metadata dinámica basada en atributos seleccionados
    metadata = {"empresa_id": empresa_id}
    if "title" in atributos:
        metadata["title"] = product_name
    if "description" in atributos:
        metadata["description"] = description
    if "slug" in atributos:
        metadata["slug"] = slug
    if "price" in atributos:
        metadata["price"] = price
    if "category" in atributos:
        metadata["category"] = category_name
    if "category_slug" in atributos:
        metadata["category_slug"] = category_slug
    if "images" in atributos:
        metadata["image"] = image

    # Insertar o actualizar en Pinecone
    try:
        index.upsert(
            vectors=[
                {
                    "id": str(product_id),
                    "values": embedding_vector,
                    "metadata": metadata
                }
            ],
            namespace=str(empresa_id)
        )
        print(f"✅ Producto {product_id} insertado en índice '{index_name}'")
        return True
    except Exception as e:
        print(f"❌ Error al insertar producto {product_id} en Pinecone: {str(e)}")
        return False


def delete_all_products_by_empresa_id(empresa_id: int, index_name: str):
    with SessionLocal() as db:
        empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
        if not empresa or not empresa.api_key_pinecone:
            raise ValueError("❌ Empresa o API Key no válida")

    pc = Pinecone(api_key=empresa.api_key_pinecone)
    index = pc.Index(index_name)
    index.delete(delete_all=True, namespace=str(empresa_id))

    print(f"🗑️ Productos eliminados para empresa {empresa_id} en índice '{index_name}'")
    return {"message": f"✅ Productos eliminados del índice '{index_name}' correctamente"}


def buscar_productos_relacionados(mensaje_usuario: str, empresa_id: int) -> List[dict]:
    with SessionLocal() as db:
        empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
        if not empresa or not empresa.api_key_pinecone or not empresa.api_key_openai:
            return []

    pc = Pinecone(api_key=empresa.api_key_pinecone)
    client = OpenAI(api_key=empresa.api_key_openai)

    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=mensaje_usuario
    )
    embedding_vector = response.data[0].embedding

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
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    indices = pc.list_indexes()
    return [idx['name'] for idx in indices]
