from agent.openai_agent import generate_response
from pinecone_module.pinecone_manager import search_similar_products


def consultar_agente_subordinado(query, empresa_id):
    """
    El agente subordinado interpreta la intención y busca productos en Pinecone.
    """
    productos_relevantes = search_similar_products(query=query, top_k=5, empresa_id=empresa_id)

    productos_texto = "\n".join([
        f"• {p.get('title', 'Sin título')} (Precio: ${p.get('price', 'N/A')})\nDescripción: {p.get('description', '')}" for p in productos_relevantes
    ])

    prompt_subordinado = f"""
    Eres un agente de búsqueda especializado en productos de una tienda. 
    El cliente ha realizado la siguiente consulta: "{query}".

    A continuación te presento los productos más relevantes encontrados:
    {productos_texto}

    Elige el producto más apropiado de esta lista según la consulta. Resume tu sugerencia en una frase clara.
    """

    respuesta_subordinado = generate_response(prompt_subordinado)
    return respuesta_subordinado


def revisar_respuesta_agente_lider(query, respuesta_subordinado):
    """
    El agente líder revisa y mejora la respuesta del subordinado antes de entregarla al cliente final.
    """
    prompt_lider = f"""
    Actúas como un supervisor experto en atención al cliente para una tienda de ecommerce.

    El cliente ha consultado: "{query}".
    Tu asistente subordinado ha propuesto esta respuesta: "{respuesta_subordinado}".

    Revisa y mejora esa respuesta para que sea clara, empática y útil al cliente final.
    Añade un cierre amable si corresponde.
    """

    respuesta_final = generate_response(prompt_lider)
    return respuesta_final


def interact_with_agent(query, empresa_id):
    """
    Proceso jerárquico completo: Subordinado responde, líder revisa.
    """
    respuesta_sub = consultar_agente_subordinado(query, empresa_id)
    respuesta_lider = revisar_respuesta_agente_lider(query, respuesta_sub)
    return respuesta_lider