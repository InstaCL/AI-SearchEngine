# sync_test.py

from client.fetch_products import fetch_products
from pinecone_module.pinecone_manager import insert_or_update_product

def main():
    print("🔄 Sincronización de Productos a Pinecone")
    try:
        empresa_id = int(input("Ingresa el ID de la empresa: "))
    except ValueError:
        print("⚠️ El ID de la empresa debe ser un número entero.")
        return

    productos = fetch_products()
    if not productos:
        print("⚠️ No se encontraron productos en la API.")
        return

    print(f"📦 Sincronizando {len(productos)} productos para empresa_id={empresa_id}...\n")

    for producto in productos:
        insert_or_update_product(
            product_id=producto["id"],
            product_name=producto["title"],
            description=producto["description"],
            slug=producto["slug"],
            price=producto["price"],
            category_name=producto["category_name"],
            category_slug=producto["category_slug"],
            image=producto["image"],
            empresa_id=empresa_id
        )

    print(f"\n✅ Sincronización completada para empresa_id={empresa_id}")

if __name__ == "__main__":
    main()
