from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Empresa
from client.fetch_products import fetch_products, generar_texto_producto
from pinecone_module.pinecone_manager import insert_or_update_product, delete_all_products_by_empresa_id
from routers.ws_sync_router import websocket_connections
import asyncio

router = APIRouter(prefix="/sync", tags=["Sincronización"])

@router.post("/empresa-productos/{empresa_id}")
async def sync_productos_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa or not empresa.indice_pinecone:
        raise HTTPException(status_code=404, detail="❌ Empresa o índice no encontrada")

    # Usar el endpoint personalizado de la empresa
    productos = fetch_products(endpoint_url=empresa.endpoint_productos)
    if not productos:
        return {"message": "⚠️ No se encontraron productos para sincronizar"}

    logs = []

    for producto in productos:
        # Generar texto dinámico para embedding basado en atributos seleccionados
        texto = generar_texto_producto(producto, empresa)
        if not texto:
            continue  # saltar productos vacíos

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

        # Enviar mensaje de progreso por WebSocket si hay conexión activa
        websocket = websocket_connections.get(empresa_id)
        if websocket:
            try:
                await websocket.send_json(log)
                await asyncio.sleep(0.05)
            except:
                pass

    return {
        "message": f"✅ Productos sincronizados correctamente en el índice '{empresa.indice_pinecone}'",
        "total": len(logs),
        "productos": logs
    }

@router.delete("/empresa-productos/{empresa_id}")
def eliminar_productos_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa or not empresa.indice_pinecone:
        raise HTTPException(status_code=404, detail="❌ Empresa o índice no encontrada")

    return delete_all_products_by_empresa_id(empresa_id, index_name=empresa.indice_pinecone)