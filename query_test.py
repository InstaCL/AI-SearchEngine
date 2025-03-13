# query_test.py

from agent.chat_interface import interact_with_agent

def main():
    print("🔍 Consulta al Agente IA de AI-SearchEngine")
    query = input("Escribe tu pregunta: ")
    try:
        empresa_id = int(input("Ingresa el ID de la empresa: "))
    except ValueError:
        print("⚠️ El ID de la empresa debe ser un número entero.")
        return

    print("\n📡 Enviando consulta al agente...\n")
    respuesta = interact_with_agent(query, empresa_id=empresa_id)
    print("🧠 Respuesta del Agente IA:\n")
    print(respuesta)

if __name__ == "__main__":
    main()
    