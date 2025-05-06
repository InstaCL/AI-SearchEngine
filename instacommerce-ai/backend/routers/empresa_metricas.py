from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import HistorialConversacion, Empresa
from backend.routers.auth_utils import obtener_empresa_actual
from pinecone import Pinecone, ServerlessSpec
from config.settings import settings

router = APIRouter(prefix="/empresa", tags=["Métricas Cliente"])

# Inicializar Pinecone
pinecone = Pinecone(api_key=settings.PINECONE_API_KEY)

@router.get("/metricas")
def obtener_metricas(empresa: Empresa = Depends(obtener_empresa_actual), db: Session = Depends(get_db)):
    # Total de conversaciones
    total_conversaciones = db.query(HistorialConversacion).filter(HistorialConversacion.empresa_id == empresa.id).count()

    # Total de productos en Pinecone (solo si el índice está creado)
    total_productos = 0
    if empresa.indice_pinecone:
        try:
            index = pinecone.Index(empresa.indice_pinecone)
            stats = index.describe_index_stats()
            total_productos = stats.to_dict().get('total_vector_count', 0)
        except Exception:
            total_productos = 0

    # Simulación de estado del entrenamiento
    estado_entrenamiento = "pendiente" if not empresa.atributos_sincronizacion else "completo"

    return {
        "total_conversaciones": total_conversaciones,
        "total_productos": total_productos,
        "estado_entrenamiento": estado_entrenamiento
    }
