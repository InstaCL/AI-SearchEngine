# verificar_pinecone_empresa2.py

from pinecone import Pinecone
from backend.database.database import SessionLocal
from backend.database.models import Empresa

# Obtener las credenciales de la empresa 1
db = SessionLocal()
empresa = db.query(Empresa).filter(Empresa.id == 1).first()

if not empresa:
    print("❌ Empresa 1 no encontrada en la base de datos.")
    exit()

# Conectar a Pinecone con la API Key de la empresa 1
pc = Pinecone(api_key=empresa.api_key_pinecone)
index = pc.Index("ai-searchengine-productos")

# Listar vectores en el namespace 1
print(f"🔎 Consultando vectores en el namespace '1'...")
result = index.describe_index_stats()
namespaces = result.get("namespaces", {})

if "1" in namespaces and namespaces["1"]["vector_count"] > 0:
    print(f"✅ Namespace '1' contiene {namespaces['1']['vector_count']} productos indexados.")
else:
    print("⚠️ Namespace '1' no tiene productos indexados.")
