from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Empresa
from client.fetch_products import fetch_products
from pinecone_module.pinecone_manager import insert_or_update_product, delete_all_products_by_empresa_id
from routers.ws_sync_router import websocket_connections
import asyncio

router = APIRouter(prefix="/sync", tags=["Sincronización"])

@router.post("/empresa-productos/{empresa_id}")
async def sync_productos_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa or not empresa.indice_pinecone:
        raise HTTPException(status_code=404, detail="❌ Empresa o índice no encontrada")

    productos = fetch_products()
    if not productos:
        return {"message": "⚠️ No se encontraron productos para sincronizar"}

    logs = []

    for producto in productos:
        insert_or_update_product(
            product_id=producto["id"],
            product_name=producto["title"],
            description=producto["description"],
            slug=producto["slug"],
            price=producto["price"],
            category_name=producto["category"]["name"],
            category_slug=producto["category"]["slug"],
            image=producto["images"][0] if producto["images"] else "",
            empresa_id=empresa_id,
            index_name=empresa.indice_pinecone
        )

        log = {
            "title": producto["title"],
            "price": producto["price"],
            "category": producto["category"]["name"]
        }
        logs.append(log)

        # Enviar mensaje de progreso por WebSocket si hay conexión activa
        websocket = websocket_connections.get(empresa_id)
        if websocket:
            try:
                await websocket.send_json(log)
                await asyncio.sleep(0.05)  # ligera pausa opcional para no saturar
            except:
                pass

    return {
        "message": f"✅ Productos sincronizados correctamente en el índice '{empresa.indice_pinecone}'",
        "total": len(productos),
        "productos": logs
    }

@router.delete("/empresa-productos/{empresa_id}")
def eliminar_productos_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa or not empresa.indice_pinecone:
        raise HTTPException(status_code=404, detail="❌ Empresa o índice no encontrada")

    return delete_all_products_by_empresa_id(empresa_id, index_name=empresa.indice_pinecone)