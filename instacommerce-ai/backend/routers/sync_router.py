from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Empresa
from client.fetch_products import fetch_products
from pinecone_module.pinecone_manager import insert_or_update_product, delete_all_products_by_empresa_id

router = APIRouter(prefix="/sync", tags=["Sincronización"])

@router.post("/empresa-productos/{empresa_id}")
def sync_productos_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="❌ Empresa no encontrada")

    productos = fetch_products()
    if not productos:
        return {"message": "⚠️ No se encontraron productos para sincronizar"}

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
            empresa_id=empresa_id
        )

    return {"message": "✅ Productos sincronizados correctamente", "total": len(productos)}

@router.delete("/empresa-productos/{empresa_id}")
def eliminar_productos_empresa(empresa_id: int):
    return delete_all_products_by_empresa_id(empresa_id)
