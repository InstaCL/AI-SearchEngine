from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.database.models import Empresa
import requests

router = APIRouter(prefix="/admin/configuracion", tags=["Admin Configuración"])

@router.get("/atributos-disponibles/{empresa_id}")
def obtener_atributos_disponibles_admin(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa or not empresa.endpoint_productos:
        raise HTTPException(status_code=404, detail="Empresa no encontrada o sin endpoint")

    try:
        response = requests.get(empresa.endpoint_productos, timeout=10)
        productos = response.json()

        if not productos or not isinstance(productos, list):
            raise ValueError("Respuesta de productos inválida")

        atributos_set = set()
        for producto in productos[:30]:
            if isinstance(producto, dict):
                atributos_set.update(producto.keys())

        atributos = sorted(list(atributos_set))
        return {"atributos": atributos}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener atributos: {str(e)}")
