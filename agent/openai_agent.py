import openai
import os
from config.settings import OPENAI_API_KEY
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# Configurar la API de OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# 📌 Prompt del asistente para mejorar las respuestas
SYSTEM_PROMPT = """
Eres un asistente especializado en ventas de productos tecnológicos en una tienda eCommerce.
Tu tarea es ayudar a los clientes a encontrar productos según sus necesidades, responder preguntas sobre especificaciones técnicas
y recomendar ofertas y productos populares.
Si no tienes información sobre un producto, sugiere otras opciones disponibles y evita dar respuestas incorrectas.
Siempre responde de forma clara y profesional, usando un tono amigable y confiable.
"""

def generate_response(query, products=None, model="gpt-4o"):
    """
    Genera una respuesta de OpenAI usando contexto de productos si está disponible.
    """
    try:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=query),
        ]

        if products:
            product_list = "\n".join([f"- {p}" for p in set(products)])  # Evita productos repetidos
            messages.append(AIMessage(content=f"Aquí tienes algunas laptops en oferta:\n{product_list}"))
        else:
            messages.append(AIMessage(content="No encontré laptops en oferta en este momento, pero dime qué buscas y te ayudaré a encontrar la mejor opción."))

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT},
                      {"role": "user", "content": query}]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error en la generación de respuesta: {e}"

