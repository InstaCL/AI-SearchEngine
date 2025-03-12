import pinecone
import openai
import os
from config.settings import PINECONE_API_KEY, PINECONE_INDEX, OPENAI_API_KEY

# Configurar OpenAI
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Conectar a Pinecone
pinecone_client = pinecone.Pinecone(api_key=PINECONE_API_KEY)
index = pinecone_client.Index(PINECONE_INDEX)  # Usar índice configurado

def generate_embedding(text):
    """
    Genera embeddings para el texto usando OpenAI.
    """
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-3-large"
    )
    return response.data[0].embedding

def insert_product(product_id, product_name, description, empresa_id=None):
    """
    Inserta un producto en Pinecone, incluyendo el empresa_id en los metadatos.
    """
    embedding = generate_embedding(product_name + " " + description)

    # Validación opcional para asegurar que los embeddings tienen 3072 dimensiones
    from config.settings import PINECONE_DIMENSIONS
    assert len(embedding) == PINECONE_DIMENSIONS, "⚠️ Dimensiones del embedding incorrectas"

    metadata = {
        "title": product_name,
        "description": description
    }

    if empresa_id:
        metadata["empresa_id"] = str(empresa_id)

    index.upsert(vectors=[{
        "id": str(product_id),
        "values": embedding,
        "metadata": metadata
    }])

    print(f"✅ Producto insertado en Pinecone: {product_name}")

def search_similar_products(query, top_k=5, empresa_id=None):
    """
    Realiza una búsqueda en Pinecone y devuelve productos relevantes filtrados por empresa_id.
    """
    query_embedding = generate_embedding(query)

    filter_query = {}
    if empresa_id:
        filter_query = {"empresa_id": {"$eq": str(empresa_id)}}

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter=filter_query
    )

    filtered_products = []
    for match in results.matches:
        metadata = match.metadata
        title = metadata.get("title", "Producto sin título")
        filtered_products.append(title)

    return filtered_products

def delete_products_by_empresa(empresa_id):
    """
    Elimina todos los productos en Pinecone relacionados a una empresa específica.
    """
    # Usamos un vector dummy para hacer un query masivo con filtro
    results = index.query(
        vector=[0.0] * 1536,  # vector dummy
        top_k=10000,
        include_metadata=True,
        filter={"empresa_id": {"$eq": str(empresa_id)}}
    )

    vector_ids = [match["id"] for match in results["matches"]]

    if vector_ids:
        index.delete(ids=vector_ids)
        print(f"🗑️ Eliminados {len(vector_ids)} vectores para empresa_id {empresa_id}")
    else:
        print(f"⚠️ No se encontraron productos para eliminar en empresa_id {empresa_id}")

    return len(vector_ids)
