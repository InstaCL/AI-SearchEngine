from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, datetime
from backend.database.database import get_db
from backend.database.models import Empresa, HistorialConversacion
from backend.config import settings
from pinecone import Pinecone

router = APIRouter(tags=["Admin Métricas"])

# Inicializa cliente Pinecone con tu API KEY desde settings
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

@router.get("/metricas-globales")
def metricas_globales(db: Session = Depends(get_db)):
    # 🏢 Empresas registradas
    total_empresas = db.query(Empresa).count()

    # 💬 Conversaciones del día actual
    hoy = date.today()
    conversaciones_hoy = db.query(HistorialConversacion).filter(
        HistorialConversacion.timestamp >= datetime.combine(hoy, datetime.min.time()),
        HistorialConversacion.timestamp <= datetime.combine(hoy, datetime.max.time())
    ).count()

    # 🔍 Productos indexados en Pinecone (sumando todos los índices registrados)
    productos_indexados = 0
    indices = pc.list_indexes()

    for empresa in db.query(Empresa).filter(Empresa.indice_pinecone.isnot(None)).all():
        if empresa.indice_pinecone in indices:
            index = pc.Index(empresa.indice_pinecone)
            stats = index.describe_index_stats()
            productos_indexados += stats.get("total_vector_count", 0)

    return {
        "total_empresas": total_empresas,
        "productos_indexados": productos_indexados,
        "conversaciones_hoy": conversaciones_hoy,
        "timestamp": datetime.utcnow().isoformat()
    }
