from typing import List
from pinecone import Pinecone
from openai import OpenAI
from database.models import Empresa
from database.database import SessionLocal
from config.settings import settings
import tiktoken

# Constantes
MAX_TOKENS = 8191
MAX_METADATA_BYTES = 40960  # 40KB
EMBEDDING_MODEL = "text-embedding-3-large"

# Utilidades
def contar_tokens(texto: str) -> int:
    encoding = tiktoken.encoding_for_model(EMBEDDING_MODEL)
    return len(encoding.encode(texto))

def dividir_texto(texto: str, max_tokens: int = MAX_TOKENS) -> List[str]:
    encoding = tiktoken.encoding_for_model(EMBEDDING_MODEL)
    tokens = encoding.encode(texto)
    partes = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [encoding.decode(p) for p in partes]

def generar_embeddings(textos: List[str], client: OpenAI) -> List[List[float]]:
    try:
        respuesta = client.embeddings.create(model=EMBEDDING_MODEL, input=textos)
        return [r.embedding for r in respuesta.data]
    except Exception as e:
        print(f"❌ Error generando embeddings: {str(e)}")
        return []

# Inserción principal
def insert_or_update_product(
    index_name: str,
    product_id: int,
    product_name: str,
    description: str,
    slug: str,
    price: float,
    category_name: str,
    category_slug: str,
    image: str,
    empresa_id: int,
):
    if not settings.OPENAI_API_KEY or not settings.PINECONE_API_KEY:
        print("❌ Faltan claves de API")
        return False

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)

    try:
        index = pc.Index(index_name)
    except Exception as e:
        print(f"❌ Error conectando a Pinecone: {str(e)}")
        return False

    # Obtener configuración de la empresa
    with SessionLocal() as db:
        empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
        if not empresa:
            print(f"❌ Empresa ID {empresa_id} no encontrada")
            return False
        atributos = empresa.get_atributos_sincronizados()

    # Construcción del texto base para embedding
    texto = ""
    if "title" in atributos:
        texto += f"{product_name} "
    if "description" in atributos:
        texto += f"{description} "
    if "slug" in atributos:
        texto += f"{slug}"

    try:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=texto.strip()
        )
        embedding_vector = response.data[0].embedding
    except Exception as e:
        print(f"❌ Error generando embedding para producto {product_id}: {str(e)}")
        return False

    # Metadata respetando los atributos seleccionados
    metadata = {"empresa_id": empresa_id}
    if "title" in atributos:
        metadata["title"] = product_name
    if "description" in atributos:
        metadata["description"] = description
    if "slug" in atributos:
        metadata["slug"] = slug
    if "price" in atributos:
        metadata["price"] = price
    if "category" in atributos:
        metadata["category"] = category_name
    if "category_slug" in atributos:
        metadata["category_slug"] = category_slug
    if "images" in atributos:
        metadata["image"] = image

    # Validar tamaño de metadata
    from json import dumps
    if len(dumps(metadata).encode("utf-8")) > MAX_METADATA_BYTES:
        print(f"⚠️ Metadata del producto {product_id} excede 40KB. Producto omitido.")
        return False

    try:
        index.upsert(
            vectors=[{
                "id": str(product_id),
                "values": embedding_vector,
                "metadata": metadata
            }],
            namespace=str(empresa_id)
        )
        print(f"✅ Producto {product_id} insertado en índice '{index_name}'")
        return True
    except Exception as e:
        print(f"❌ Error subiendo producto {product_id} a Pinecone: {str(e)}")
        return False

# Eliminar todos los vectores de una empresa
def delete_all_products_by_empresa_id(empresa_id: int, index_name: str):
    with SessionLocal() as db:
        empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
        if not empresa or not empresa.api_key_pinecone:
            raise ValueError("❌ Empresa o API Key no válida")

    pc = Pinecone(api_key=empresa.api_key_pinecone)
    index = pc.Index(index_name)
    index.delete(delete_all=True, namespace=str(empresa_id))

    print(f"🗑️ Productos eliminados para empresa {empresa_id} en índice '{index_name}'")
    return {"message": f"✅ Productos eliminados del índice '{index_name}' correctamente"}

# Búsqueda de productos relacionados
def buscar_productos_relacionados(mensaje_usuario: str, empresa_id: int) -> List[dict]:
    with SessionLocal() as db:
        empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
        if not empresa or not empresa.api_key_pinecone or not empresa.api_key_openai:
            return []

    pc = Pinecone(api_key=empresa.api_key_pinecone)
    client = OpenAI(api_key=empresa.api_key_openai)

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=mensaje_usuario
    )
    embedding_vector = response.data[0].embedding

    index = pc.Index("ai-searchengine-productos")
    resultados = index.query(
        vector=embedding_vector,
        top_k=5,
        namespace=str(empresa_id),
        include_metadata=True
    )

    productos = []
    for match in resultados.matches:
        metadata = match.metadata
        productos.append({
            "title": metadata.get("title"),
            "price": metadata.get("price"),
            "description": metadata.get("description", "")
        })

    return productos

# Listar índices disponibles
def obtener_indices_pinecone():
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    return [index.name for index in pc.list_indexes()]

def listar_indices_disponibles() -> list[str]:
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    indices = pc.list_indexes()
    return [idx['name'] for idx in indices]
