import os
from pinecone import Pinecone
from database.database import SessionLocal
from database.models import Empresa

# Cambia este ID según corresponda
EMPRESA_ID = 1

# Obtener API Key desde base de datos
db = SessionLocal()
empresa = db.query(Empresa).filter(Empresa.id == EMPRESA_ID).first()

if not empresa:
    raise Exception("❌ Empresa no encontrada")

# Inicializa nuevo cliente Pinecone
pc = Pinecone(api_key=empresa.api_key_pinecone)

# Conecta al índice
index = pc.Index("ai-searchengine-productos")

# Obtener estadísticas del índice
stats = index.describe_index_stats()
namespace_info = stats.get("namespaces", {}).get(str(EMPRESA_ID), {})

print(f"🔎 Verificando namespace '{EMPRESA_ID}' en Pinecone...")

if not namespace_info:
    print("⚠️ No hay productos indexados para esta empresa.")
else:
    print(f"✅ Productos encontrados: {namespace_info.get('vector_count', 0)} vectores en Pinecone")
