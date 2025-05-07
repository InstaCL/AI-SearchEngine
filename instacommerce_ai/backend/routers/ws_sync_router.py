from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict

router = APIRouter()

# Diccionario para mantener conexiones activas por empresa_id
websocket_connections: Dict[int, WebSocket] = {}

@router.websocket("/ws/sync/{empresa_id}")
async def websocket_sync(websocket: WebSocket, empresa_id: int):
    await websocket.accept()
    websocket_connections[empresa_id] = websocket
    try:
        while True:
            await websocket.receive_text()  # Mantener conexión activa
    except WebSocketDisconnect:
        websocket_connections.pop(empresa_id, None)
