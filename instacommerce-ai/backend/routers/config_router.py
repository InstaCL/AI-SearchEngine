from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Empresa
from pydantic import BaseModel
from pinecone_module.pinecone_manager import listar_indices_disponibles
from typing import List
from .auth_utils import obtener_empresa_actual
import requests


router = APIRouter()

# -------- MODELOS --------
class CredencialesUpdate(BaseModel):
    api_key_openai: str
    api_key_pinecone: str
    endpoint_productos: str

class AtributosSeleccionadosRequest(BaseModel):
    atributos: List[str]

# -------- ENDPOINTS EXISTENTES --------
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
    indices = listar_indices_disponibles()
    return {"indices": indices}

# -------- NUEVOS ENDPOINTS PARA ATRIBUTOS --------
@router.get("/configuracion/atributos-disponibles")
def obtener_atributos_disponibles(
    db: Session = Depends(get_db),
    empresa: Empresa = Depends(obtener_empresa_actual)
):
    if not empresa or not empresa.endpoint_productos:
        raise HTTPException(status_code=400, detail="Empresa no configurada o endpoint no definido")

    try:
        response = requests.get(empresa.endpoint_productos, timeout=10)
        productos = response.json()
        if not productos or not isinstance(productos, list) or not productos[0]:
            raise ValueError("Respuesta inválida o vacía")

        primer_producto = productos[0]
        atributos = list(primer_producto.keys())

        return {"atributos": atributos}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener atributos: {str(e)}")

@router.post("/configuracion/atributos-seleccionados")
def guardar_atributos_seleccionados(
    data: AtributosSeleccionadosRequest,
    empresa: Empresa = Depends(obtener_empresa_actual),
    db: Session = Depends(get_db)
):
    if not empresa:
        raise HTTPException(status_code=401, detail="No autorizado")

    empresa.set_atributos_sincronizados(data.atributos)
    db.commit()

    return {"mensaje": "Atributos sincronizados guardados correctamente"}

@router.get("/configuracion/atributos-seleccionados")
def obtener_atributos_seleccionados(empresa: Empresa = Depends(obtener_empresa_actual)):
    """
    Devuelve la lista de atributos que la empresa ha guardado para sincronizar.
    """
    try:
        import json
        atributos = json.loads(empresa.atributos_sincronizacion or "[]")
    except:
        atributos = []
    return {"atributos": atributos}