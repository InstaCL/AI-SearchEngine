# routers/productos_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Empresa
import requests

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get("/atributos/{empresa_id}")
def obtener_atributos_api(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="❌ Empresa no encontrada")

    if not empresa.endpoint_productos:
        raise HTTPException(status_code=400, detail="⚠️ Endpoint de productos no registrado")

    try:
        response = requests.get(empresa.endpoint_productos)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="⚠️ No se pudo acceder al endpoint de productos")
        productos = response.json()
        if not productos or not isinstance(productos, list):
            raise HTTPException(status_code=400, detail="⚠️ Formato inválido de productos")
        atributos = list(productos[0].keys())
        return {"atributos_disponibles": atributos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Error al obtener atributos: {str(e)}")
