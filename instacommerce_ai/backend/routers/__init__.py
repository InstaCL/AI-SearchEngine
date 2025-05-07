# routers/__init__.py

from .empresas_router import router as empresas_router
from .auth_router import router as auth_router
from .config_router import router as config_router
from .sync_router import router as sync_router
from .chat_router import router as chat_router
from .empresa_register import router as empresa_register
from .historial_router import router as historial_router

# Aquí podrías agregar los próximos routers: subordinado_router, lider_router, etc.

all_routers = [
    ("empresas", empresas_router, "Empresas"),
    ("auth", auth_router, "Autenticación"),
    ("configuracion", config_router, "Configuración Técnica"),
    ("sync", sync_router, "Sincronización de Productos"),
    ("chat", chat_router, "IA - Interacción Cliente"),
    ("historial", historial_router, "Historial de Conversaciones"),  # ✅ Nuevo router agregado
]
