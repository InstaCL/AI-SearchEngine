import openai
import os
from config.settings import OPENAI_API_KEY

# Configurar la API de OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_response(prompt, model="gpt-4o"):
    """
    Envía un prompt a OpenAI y devuelve la respuesta generada.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en la generación de respuesta: {e}"
