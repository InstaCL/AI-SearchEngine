from agent.openai_agent import generate_response
from pinecone_module.pinecone_manager import search_similar_products

def interact_with_agent(query):
    """
    Busca productos en Pinecone antes de consultar a OpenAI, optimizando la respuesta.
    """
    print("\n🤖 AI-SearchEngine: Buscando productos en Pinecone...")

    # Buscar productos en Pinecone
    similar_products = search_similar_products(query, top_k=5)

    if not similar_products:
        print("❌ No se encontraron productos similares en Pinecone.")
        prompt = f"""Un usuario está buscando: '{query}', pero la base de datos no tiene productos exactos para esa descripción.

En lugar de inventar productos, sugiere una solución alternativa o pregunta si quiere explorar otra categoría de productos que sí estén disponibles.
"""
        response = generate_response(prompt)
    else:
        product_list = "\n".join(f"- {product}" for product in similar_products)
        prompt = f"""Estos son los productos más relevantes encontrados en la base de datos para la consulta: '{query}'

{product_list}

Genera una respuesta profesional explicando por qué estos productos pueden ser útiles para la necesidad del usuario. Si no hay coincidencias exactas, sugiere productos similares con una breve explicación.
"""
        response = generate_response(prompt)

    print("\n🛒 Productos recomendados:")
    print(response)

    return response
