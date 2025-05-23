from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers del sistema (import local sin prefijo)
from backend.routers.empresas_router import router as empresas_router
from backend.routers.chat_router import router as chat_router
from backend.routers.config_router import router as config_router
from backend.routers.sync_router import router as sync_router
from backend.routers.ws_sync_router import router as ws_sync_router
from backend.routers.prueba_router import router as prueba_router
from backend.routers.empresa_login import router as login_router
from backend.routers.registro_router import router as registro_router
from backend.routers.empresa_perfil import router as empresa_perfil_router
from backend.routers.admin_login import router as admin_login_router
from backend.routers.empresa_metricas import router as metricas_router
from backend.routers.admin_metricas_router import router as admin_metricas_router
from backend.routers.admin_configuracion import router as admin_config_router

# App FastAPI
app = FastAPI(title="Instacommerce AI - Backend")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://tudominio.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(empresas_router)
app.include_router(chat_router)
app.include_router(config_router)
app.include_router(sync_router)
app.include_router(ws_sync_router)
app.include_router(prueba_router, prefix="/prueba")
app.include_router(login_router, prefix="/empresa")
app.include_router(admin_login_router, prefix="/admin")
app.include_router(registro_router)
app.include_router(empresa_perfil_router)
app.include_router(metricas_router)
app.include_router(admin_metricas_router, prefix="/admin")
app.include_router(admin_config_router)

# Ruta raíz
@app.get("/")
def home():
    return {"message": "🚀 Bienvenido a Instacommerce AI Backend"}
