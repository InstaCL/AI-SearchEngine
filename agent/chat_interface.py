from agent.openai_agent import generate_response
from pinecone_module.pinecone_manager import search_similar_products

def interact_with_agent(query):
    """
    Busca productos en Pinecone antes de consultar a OpenAI.
    """
    print("\n🤖 AI-SearchEngine: Buscando productos en Pinecone...")

    # Buscar productos en Pinecone
    similar_products = search_similar_products(query, top_k=5)

    if not similar_products:
        print("❌ No se encontraron productos similares en Pinecone.")
        return "No se encontraron productos."

    # Construir el prompt con los productos encontrados
    product_list = "\n".join(f"- {product}" for product in similar_products)
    prompt = f"""Los siguientes productos fueron encontrados en la base de datos:
{product_list}

Basado en estos productos, responde a la consulta del usuario:
{query}
"""

    # Obtener respuesta de OpenAI
    response = generate_response(prompt)

    print("\n🛒 Productos recomendados:")
    print(response)

    return response
