from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Empresa
from pydantic import BaseModel
from pinecone_module.pinecone_manager import listar_indices_disponibles  # ✅

router = APIRouter()

class CredencialesUpdate(BaseModel):
    api_key_openai: str
    api_key_pinecone: str
    endpoint_productos: str

@router.put("/configuracion/credenciales/{empresa_id}")
def actualizar_credenciales(empresa_id: int, credenciales: CredencialesUpdate, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    empresa.api_key_openai = credenciales.api_key_openai
    empresa.api_key_pinecone = credenciales.api_key_pinecone
    empresa.endpoint_productos = credenciales.endpoint_productos
    db.commit() 

    return {"message": "🔐 Credenciales actualizadas correctamente"}

@router.get("/configuracion/indices-pinecone")
def obtener_indices():
    indices = listar_indices_disponibles()  # ✅ Corrección aquí
    return {"indices": indices}
