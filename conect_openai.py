import os
from langchain_openai import ChatOpenAI

def get_openai_api_key():
    """Solicita la API key de OpenAI si no está configurada en las variables de entorno"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Introduce tu API Key de OpenAI: ")
        os.environ["OPENAI_API_KEY"] = api_key
    return api_key

# Configuración del modelo
api_key = get_openai_api_key()
model = ChatOpenAI(model='gpt-4o', openai_api_key=api_key)