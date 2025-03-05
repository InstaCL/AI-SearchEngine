import pinecone
import openai
import os
from config.settings import PINECONE_API_KEY, PINECONE_INDEX, OPENAI_API_KEY

# Configurar OpenAI
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Conectar a Pinecone con la nueva API
pinecone_client = pinecone.Pinecone(api_key=PINECONE_API_KEY)
index = pinecone_client.Index(PINECONE_INDEX)

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
    Busca productos similares en Pinecone basado en la consulta del usuario.
    """
    query_embedding = generate_embedding(query)
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

    if results and results.get("matches"):
        return [match["metadata"].get("title", "Producto sin título") for match in results["matches"]]
    else:
        return []
