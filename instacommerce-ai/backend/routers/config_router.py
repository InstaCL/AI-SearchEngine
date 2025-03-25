from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Empresa
from schemas import CredencialesUpdate

router = APIRouter(prefix="/config", tags=["Configuración Técnica"])

@router.put("/{empresa_id}")
def actualizar_configuracion_tecnica(empresa_id: int, config: CredencialesUpdate, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="❌ Empresa no encontrada")

    empresa.api_key_openai = config.api_key_openai
    empresa.api_key_pinecone = config.api_key_pinecone
    empresa.endpoint_productos = config.endpoint_productos

    db.commit()
    return {"message": "✅ Configuración actualizada", "empresa_id": empresa.id}
