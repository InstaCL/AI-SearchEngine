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

def insert_product(product_id, product_name, description):
    """
    Inserta un producto en Pinecone.
    """
    embedding = generate_embedding(product_name + " " + description)
    index.upsert(vectors=[{"id": str(product_id), "values": embedding, "metadata": {"title": product_name, "description": description}}])
    print(f"✅ Producto insertado en Pinecone: {product_name}")

def search_similar_products(query, top_k=5):
    """
    Realiza una búsqueda en Pinecone y devuelve productos relevantes.
    """
    # Convertimos la consulta en un embedding usando el mismo modelo de OpenAI
    query_embedding = generate_embedding(query)

    # Ejecutamos la búsqueda en Pinecone
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

    # Filtrar solo laptops
    filtered_products = []
    for match in results["matches"]:
        title = match["metadata"].get("title", "Producto sin título")
        description = match["metadata"].get("description", "")

        if "laptop" in title.lower() or "laptop" in description.lower():
            filtered_products.append(title)

    return filtered_products
    