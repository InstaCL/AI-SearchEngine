from agent.subordinate_agent import generar_respuesta_subordinado
from agent.leader_agent import enriquecer_respuesta_lider

def interact_with_agent(mensaje_usuario, empresa_id):
    respuesta_subordinado = generar_respuesta_subordinado(mensaje_usuario, empresa_id)
    respuesta_final = enriquecer_respuesta_lider(mensaje_usuario, respuesta_subordinado, empresa_id)
    return respuesta_final
