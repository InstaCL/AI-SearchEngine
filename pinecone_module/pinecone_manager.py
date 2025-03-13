# pinecone_module/pinecone_manager.py

import pinecone
import openai
from config.settings import PINECONE_API_KEY, PINECONE_INDEX, PINECONE_DIMENSIONS, OPENAI_API_KEY

# Configurar OpenAI
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Conectar a Pinecone
pinecone_client = pinecone.Pinecone(api_key=PINECONE_API_KEY)
index = pinecone_client.Index(PINECONE_INDEX)

def generate_embedding(text):
    """
    Genera embeddings para el texto usando OpenAI.
    """
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-3-large"
    )
    return response.data[0].embedding

def insert_or_update_product(product_id, product_name, description, slug="", price=0, category_name="", category_slug="", image="", empresa_id=None):
    """
    Inserta o actualiza un producto enriquecido en Pinecone con metadatos completos.
    """
    embedding = generate_embedding(f"{product_name} {description} {category_name} {slug}")

    assert len(embedding) == PINECONE_DIMENSIONS, "⚠️ Dimensiones incorrectas para Pinecone"

    metadata = {
        "title": product_name,
        "description": description,
        "slug": slug,
        "price": price,
        "category_name": category_name,
        "category_slug": category_slug,
        "image": image
    }

    if empresa_id:
        metadata["empresa_id"] = str(empresa_id)

    vector_id = f"{empresa_id}_{product_id}"  # clave única por empresa + producto

    index.upsert(vectors=[{
        "id": vector_id,
        "values": embedding,
        "metadata": metadata
    }])

    print(f"✅ Producto insertado/actualizado en Pinecone: {product_name} (ID: {vector_id})")

def search_similar_products(query, top_k=5, empresa_id=None):
    query_embedding = generate_embedding(query)

    filter_query = {"empresa_id": {"$eq": str(empresa_id)}} if empresa_id else {}

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter=filter_query
    )

    return [match.metadata for match in results.matches]

def delete_all_products_by_empresa_id(empresa_id: int):
    filter_query = {"empresa_id": {"$eq": str(empresa_id)}}

    result = index.query(
        vector=[0.0] * PINECONE_DIMENSIONS,
        top_k=10000,
        include_values=False,
        include_metadata=False,
        filter=filter_query
    )

    vector_ids = [match.id for match in result.matches]

    if not vector_ids:
        print(f"⚠️ No se encontraron productos para empresa_id={empresa_id}")
        return {"message": "No se encontraron productos para eliminar", "total": 0}

    index.delete(ids=vector_ids)
    print(f"🗑️ Eliminados {len(vector_ids)} productos del índice Pinecone para empresa_id={empresa_id}")
    return {"message": "✅ Productos eliminados correctamente", "total": len(vector_ids)}
