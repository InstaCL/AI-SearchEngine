# routers/__init__.py

from .empresa_router import router as empresa_router
from .auth_router import router as auth_router
from .config_router import router as config_router
from .sync_router import router as sync_router
from .chat_router import router as chat_router
from .empresa_register import router as empresa_register


# Aquí podrías agregar los próximos routers: subordinado_router, lider_router, etc.

all_routers = [
    ("auth", auth_router, "Autenticación"),
    ("empresas", empresa_router, "Empresas"),
    ("configuracion", config_router, "Configuración Técnica"),
    ("sync", sync_router, "Sincronización de Productos"),
    ("chat", chat_router, "IA - Interacción Cliente"),
]
