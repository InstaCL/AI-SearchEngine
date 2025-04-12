import requests
from database.models import Empresa

def fetch_products(endpoint_url: str = "https://api.escuelajs.co/api/v1/products"):
    try:
        response = requests.get(endpoint_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error al obtener productos del endpoint: {str(e)}")
        return []

def generar_texto_producto(producto: dict, empresa: Empresa) -> str:
    """
    Construye el texto que será embebido en Pinecone,
    usando solo los atributos seleccionados por la empresa.
    Soporta claves anidadas usando notación 'clave.subclave'.
    """
    atributos = empresa.get_atributos_sincronizados()
    if not atributos:
        print(f"⚠️ Empresa {empresa.id} no tiene atributos seleccionados.")
        return ""

    partes = []

    for attr in atributos:
        if '.' in attr:
            # Soporte para atributos anidados como 'category.name'
            keys = attr.split('.')
            valor = producto
            for key in keys:
                valor = valor.get(key, {}) if isinstance(valor, dict) else {}
            partes.append(str(valor) if valor else "")
        else:
            partes.append(str(producto.get(attr, "")))

    texto = " ".join(partes).strip()
    
    print(f"📦 Producto ID {producto.get('id')} → Texto generado para embedding:\n{texto}\n")
    return texto
