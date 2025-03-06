import sys
import os

# Agregar la carpeta raíz del proyecto al sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from langchain_openai import OpenAIEmbeddings
from pinecone_module.pinecone_manager import query_vector

# Crear el modelo de embeddings
embed_model = OpenAIEmbeddings()

# Solicitud del usuario
consulta = "Necesito unas zapatillas de fútbol resistentes, talla 40 y económicas"

# Generar embedding de la consulta
query_vector_embedding = embed_model.embed_query(consulta)

# Buscar en Pinecone
resultados = query_vector(query_vector_embedding, top_k=5)

# Mostrar resultados
print("\nProductos recomendados:")
for match in resultados["matches"]:
    producto = match["metadata"]
    print(f"- {producto['title']} | {producto['categoria']} | Talla {producto['talla']} | Precio: {producto['precio']} | Similitud: {match['score']:.4f}")
