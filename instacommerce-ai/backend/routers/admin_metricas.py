from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Empresa
import datetime

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/metricas-globales")
def obtener_metricas_globales(db: Session = Depends(get_db)):
    total_empresas = db.query(Empresa).count()

    # Simulados (más adelante se conectarán a datos reales)
    productos_indexados = 325
    conversaciones_hoy = 48

    return {
        "total_empresas": total_empresas,
        "productos_indexados": productos_indexados,
        "conversaciones_hoy": conversaciones_hoy,
        "timestamp": datetime.datetime.utcnow()
    }
