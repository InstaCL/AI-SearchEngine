from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Empresa
from backend.client.fetch_products import fetch_products_paginated, generar_texto_producto
from backend.pinecone_module.pinecone_manager import insert_or_update_product, delete_all_products_by_empresa_id
from backend.routers.ws_sync_router import websocket_connections
import requests
import asyncio

router = APIRouter(prefix="/sync", tags=["Sincronización"])

@router.post("/empresa-productos/{empresa_id}")
async def sync_productos_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa or not empresa.indice_pinecone:
        raise HTTPException(status_code=404, detail="❌ Empresa o índice no encontrada")

    if not empresa.endpoint_productos:
        raise HTTPException(status_code=400, detail="❌ Endpoint de productos no configurado")

    logs = []
    total_importados = 0

    try:
        for producto in fetch_products_paginated(endpoint_url=empresa.endpoint_productos, limit=100):
            texto = generar_texto_producto(producto, empresa)
            if not texto:
                continue

            insert_or_update_product(
                product_id=producto.get("id"),
                product_name=producto.get("title", ""),
                description=texto,
                slug=producto.get("slug", ""),
                price=producto.get("price", 0),
                category_name=producto.get("category", {}).get("name", ""),
                category_slug=producto.get("category", {}).get("slug", ""),
                image=producto.get("images", [""])[0],
                empresa_id=empresa_id,
                index_name=empresa.indice_pinecone
            )

            log = {
                "title": producto.get("title", ""),
                "price": producto.get("price", 0),
                "category": producto.get("category", {}).get("name", "")
            }
            logs.append(log)
            total_importados += 1

            websocket = websocket_connections.get(empresa_id)
            if websocket:
                try:
                    await websocket.send_json(log)
                    await asyncio.sleep(0.02)  # ajustar si es necesario
                except:
                    pass

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Error durante la sincronización: {str(e)}")

    return {
        "message": f"✅ Se sincronizaron {total_importados} productos en el índice '{empresa.indice_pinecone}'",
        "total": total_importados,
        "productos": logs
    }

@router.delete("/empresa-productos/{empresa_id}")
def eliminar_productos_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa or not empresa.indice_pinecone:
        raise HTTPException(status_code=404, detail="❌ Empresa o índice no encontrada")

    return delete_all_products_by_empresa_id(empresa_id, index_name=empresa.indice_pinecone)

@router.get("/empresa-productos/{empresa_id}/count")
def contar_productos_endpoint(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa or not empresa.endpoint_productos:
        raise HTTPException(status_code=404, detail="Empresa o endpoint no encontrado")

    try:
        response = requests.get(empresa.endpoint_productos)
        response.raise_for_status()
        productos = response.json()
        if not isinstance(productos, list):
            raise ValueError("El endpoint no devuelve un array")

        return {"total": len(productos)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al contar productos: {str(e)}")
