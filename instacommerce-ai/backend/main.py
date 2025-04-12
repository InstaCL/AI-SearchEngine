from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importaciones de routers
from routers.empresas_router import router as empresa_router
from routers.empresa_register import router as empresa_register
from routers.chat_router import router as chat_router
from routers.config_router import router as config_router
from routers.prueba_router import router as prueba_router
from routers.sync_router import router as sync_router
from routers.ws_sync_router import router as ws_sync_router  # WebSocket para sincronización en tiempo real
from routers.empresa_login import router as empresa_login

# Inicializar la app FastAPI
app = FastAPI(title="Instacommerce AI - Backend")

app.include_router(empresa_login, prefix="/empresa")  # 👈 esto monta /empresa/login

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

# Routers montados con sus propios prefijos definidos internamente
app.include_router(empresa_router)            # /empresas
app.include_router(empresa_register)          # Registro de empresa
app.include_router(chat_router)               # Chat IA
app.include_router(config_router)             # Configuración técnica
app.include_router(sync_router)               # Sincronización manual
app.include_router(ws_sync_router)            # Sincronización WebSocket en tiempo real
app.include_router(prueba_router, prefix="/prueba", tags=["Prueba Debug"])  # Debug opcional

# Ruta raíz
@app.get("/")
def home():
    return {"message": "🚀 Bienvenido a Instacommerce AI Backend"}
