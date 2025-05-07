from typing import List

from typing import List, Dict

def validar_respuesta_subordinado(respuesta_subordinado: str, contexto: List[str], mensaje_usuario: str, productos: List[Dict]) -> str:
    if not productos:
        return "(Líder): El subordinado no encontró productos, por lo tanto no puedo enriquecer la respuesta."

    partes = ["(Líder): Gracias por tu consulta. Aquí te presento los productos que pueden interesarte:\n"]

    for idx, prod in enumerate(productos, 1):
        partes.append(
            f"🔹 Producto {idx}:\n"
            f"📌 *{prod['title']}*\n"
            f"💲 Precio: ${prod['price']}\n"
            f"📝 {prod['description']}\n"
        )

    partes.append("\n¿Te gustaría que te comparta el enlace para que revises sus características o disponibilidad?")
    return "\n".join(partes)

