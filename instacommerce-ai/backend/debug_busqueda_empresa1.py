from pinecone import Pinecone
from openai import OpenAI
from database.database import SessionLocal
from database.models import Empresa

# Cargar empresa
db = SessionLocal()
empresa = db.query(Empresa).filter(Empresa.id == 1).first()
if not empresa:
    print("❌ Empresa no encontrada.")
    exit()

# Inicializar OpenAI y Pinecone
openai = OpenAI(api_key=empresa.api_key_openai)
pc = Pinecone(api_key=empresa.api_key_pinecone)

# Crear embedding para la consulta del usuario
consulta = "Que productos tienes disponibles?"
embedding = openai.embeddings.create(
    model="text-embedding-3-large",
    input=consulta
).data[0].embedding

# Buscar en Pinecone
index = pc.Index("ai-searchengine-productos")
respuesta = index.query(
    namespace=str(empresa.id),
    vector=embedding,
    top_k=5,
    include_metadata=True
)

print("\n🔍 Resultados encontrados:")
if not respuesta.matches:
    print("⚠️ Ningún producto fue relevante.")
else:
    for i, match in enumerate(respuesta.matches):
        print(f"\n🔹 Producto {i+1}")
        print(f"  - Título: {match.metadata.get('title')}")
        print(f"  - Score: {match.score:.4f}")
