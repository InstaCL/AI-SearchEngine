from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import HistorialConversacion

router = APIRouter()

@router.get("/historial/{empresa_id}")
def obtener_historial_por_empresa(empresa_id: int, db: Session = Depends(get_db)):
    historial = db.query(HistorialConversacion).filter(
        HistorialConversacion.empresa_id == empresa_id
    ).order_by(HistorialConversacion.timestamp.desc()).all()

    if not historial:
        raise HTTPException(status_code=404, detail="❌ No se encontró historial para esta empresa.")

    return [
        {
            "chat_id": h.chat_id,
            "resumen": h.resumen,
            "productos_mencionados": h.productos_mencionados,
            "timestamp": h.timestamp
        }
        for h in historial
    ]