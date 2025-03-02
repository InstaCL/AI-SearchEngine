from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from conect_openai import model  # Importamos el modelo desde conect_openai.py

def get_chat_response():
    messages = [
        SystemMessage(content='Eres un asistente útil'),
        HumanMessage(content='Me ayudas a organizar las tareas del día?'),
        AIMessage(content='Claro! ¿Qué tareas necesitas completar hoy?'),
        HumanMessage(content='Tengo que enviar un correo importante, hacer ejercicio y estudiar para un examen'),
        AIMessage(content='Aquí tienes tu lista de tareas:\n1. Enviar correo.\n2. Hacer ejercicio.\n3. Estudiar para el examen')
    ]
    
    response = model.invoke(messages)
    return response.content