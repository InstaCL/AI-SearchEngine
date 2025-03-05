from agent.openai_agent import generate_response
from client.fetch_products import fetch_products

def interact_with_agent(query):
    """
    Función para interactuar con el agente basado en OpenAI, usando productos reales de la API.
    """
    print("\n🤖 AI-SearchEngine: Buscando productos según la consulta...")

    # Obtener los productos desde la API
    products = fetch_products()

    if not products:
        print("❌ No se pudieron obtener productos. Verifica la API.")
        return "No se encontraron productos disponibles."

    # Generar el prompt con los productos reales
    product_list = "\n".join([f"- {p['title']}: {p['description']}" for p in products[:10]])  # Limitar a 10 productos
    prompt = f"Estos son los productos disponibles:\n{product_list}\n\nCon base en estos productos, responde a la consulta: {query}"

    # Obtener respuesta de OpenAI
    response = generate_response(prompt)

    print("\n🛒 Productos recomendados:")
    print(response)

    return response
