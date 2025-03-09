import pinecone
import openai
import os
from config.settings import PINECONE_API_KEY, PINECONE_INDEX, OPENAI_API_KEY

# Configurar OpenAI
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Conectar a Pinecone con la nueva API
pinecone_client = pinecone.Pinecone(api_key=PINECONE_API_KEY)
index = pinecone_client.Index(PINECONE_INDEX)  # Corrección: Se usa el cliente para obtener el índice

def generate_embedding(text):
    """
    Genera embeddings para el texto usando OpenAI.
    """
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def insert_product(product_id, product_name, description, empresa_id=None):
    """
    Inserta un producto en Pinecone, incluyendo el empresa_id en los metadatos.
    """
    embedding = generate_embedding(product_name + " " + description)

    metadata = {
        "title": product_name,
        "description": description
    }

    if empresa_id:
        metadata["empresa_id"] = str(empresa_id)  # se guarda como string

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

    