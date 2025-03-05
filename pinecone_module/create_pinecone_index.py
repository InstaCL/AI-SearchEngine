import os
from pinecone import Pinecone, ServerlessSpec

# Obtener la API Key de Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY") or input("Introduce tu Pinecone API Key: ")

# Crear instancia de Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Definir el nombre del índice
INDEX_NAME = "mi-indice"

# Verificar si el índice ya existe
if INDEX_NAME not in pc.list_indexes().names():
    print(f"Creando el índice '{INDEX_NAME}' en Pinecone...")
    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,  # Debe coincidir con los embeddings que usarás
        metric="cosine",  # Otras opciones: "euclidean", "dotproduct"
        spec=ServerlessSpec(cloud="aws", region="us-east-1")  # Cambiamos la región a la permitida
    )
    print(f"Índice '{INDEX_NAME}' creado exitosamente.")
else:
    print(f"El índice '{INDEX_NAME}' ya existe.")
