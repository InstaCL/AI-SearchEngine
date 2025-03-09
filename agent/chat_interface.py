from agent.openai_agent import generate_response
from pinecone_module.pinecone_manager import search_similar_products

def interact_with_agent(query, empresa_id=None):
    print("🤖 AI-SearchEngine: Buscando productos en Pinecone...")

    # Buscar productos relevantes según la empresa
    similar_products = search_similar_products(query, top_k=5, empresa_id=empresa_id)

    if not similar_products:
        return "Lo siento, no encontré productos relacionados en tu catálogo. ¿Quieres que revise otra categoría o tipo de producto?"

    # Crear un mensaje personalizado para OpenAI
    prompt = f"""Eres un asistente útil de una tienda ecommerce de productos tecnológicos. 
El cliente ha preguntado: "{query}"

Estos son los productos disponibles relacionados con su consulta:
{chr(10).join([f"- {producto}" for producto in similar_products])}

Basado en esta información, responde al cliente de forma clara, útil y comercial, explicando por qué esos productos son útiles y haciendo sugerencias si es necesario.
"""

    return generate_response(prompt)
