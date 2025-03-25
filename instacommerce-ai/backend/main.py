from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importaciones de routers
from routers import all_routers
from routers.empresa_register import router as empresa_register
from routers.chat_router import router as chat_router

# Inicializar la app FastAPI
app = FastAPI(title="Instacommerce AI - Backend")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://tudominio.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir dinámicamente los routers con prefijos
for prefix, router, tag in all_routers:
    app.include_router(router, prefix=f"/{prefix}", tags=[tag])

# Routers sin prefijo
app.include_router(empresa_register, tags=["Registro de Empresa"])
app.include_router(chat_router, tags=["IA - Chat"])

# Ruta raíz
@app.get("/")
def home():
    return {"message": "🚀 Bienvenido a Instacommerce AI Backend"}
