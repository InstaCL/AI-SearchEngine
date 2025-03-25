def insert_or_update_product(**kwargs):
    print("📥 Producto insertado o actualizado (simulación)")
    return True

def delete_all_products_by_empresa_id(empresa_id: int):
    print(f"🗑️ Productos eliminados para empresa {empresa_id} (simulación)")
    return {"message": "✅ Productos eliminados correctamente"}
