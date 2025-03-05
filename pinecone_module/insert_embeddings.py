from langchain_openai import OpenAIEmbeddings
from pinecone.pinecone_manager import upsert_vector

# Crear el modelo de embeddings
embed_model = OpenAIEmbeddings()

# Texto que queremos almacenar
text = "¿Cuáles son las mejores prácticas para organizar tareas?"
vector = embed_model.embed_query(text)

# Insertar en Pinecone
upsert_vector(id="texto_1", vector=vector, metadata={"texto": text})
print("Vector insertado en Pinecone.")
