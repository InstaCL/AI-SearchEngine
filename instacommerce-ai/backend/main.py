from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers del sistema
from routers.empresas_router import router as empresas_router
from routers.chat_router import router as chat_router
from routers.config_router import router as config_router
from routers.sync_router import router as sync_router
from routers.ws_sync_router import router as ws_sync_router
from routers.prueba_router import router as prueba_router
from routers.empresa_login import router as login_router
from routers.registro_router import router as registro_router
from routers.empresa_perfil import router as empresa_perfil_router
from routers.admin_login import router as admin_login_router  # ✅ Nuevo router de admin

# App FastAPI
app = FastAPI(title="Instacommerce AI - Backend")

# ---------------------
# Middleware CORS
# ---------------------
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

# ---------------------
# Routers
# ---------------------
app.include_router(empresas_router)                        # /empresas
app.include_router(chat_router)                            # /chat
app.include_router(config_router)                          # /configuracion
app.include_router(sync_router)                            # /sync
app.include_router(ws_sync_router)                         # /ws/sync/{id}
app.include_router(prueba_router, prefix="/prueba")        # /prueba
app.include_router(login_router, prefix="/empresa")        # /empresa/login
app.include_router(admin_login_router)                     # /admin/login ✅ sin doble prefix
app.include_router(registro_router)                        # /registro
app.include_router(empresa_perfil_router)                  # /empresa/perfil

# ---------------------
# Ruta raíz
# ---------------------
@app.get("/")
def home():
    return {"message": "🚀 Bienvenido a Instacommerce AI Backend"}
