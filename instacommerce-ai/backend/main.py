from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Inicialización de la aplicación FastAPI
app = FastAPI(title="AI-SearchEngine Backend", version="1.0.0")

# Middleware CORS para permitir conexión con frontend (React en Vercel u otras URLs permitidas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringirlo después a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta raíz de prueba
@app.get("/")
def root():
    return {"message": "🚀 Bienvenido a la API de AI-SearchEngine - Instacommerce AI"}

# Importación de routers (modularización profesional)
# from routers.empresas import router as empresas_router
# from routers.configuracion import router as configuracion_router
# from routers.sync import router as sync_router
# from routers.agentes import router as agentes_router

# Registro de routers (descomentar cuando estén disponibles)
# app.include_router(empresas_router, prefix="/empresas", tags=["Empresas"])
# app.include_router(configuracion_router, prefix="/configuracion", tags=["Configuración Técnica"])
# app.include_router(sync_router, prefix="/sync", tags=["Sincronización"])
# app.include_router(agentes_router, prefix="/agentes", tags=["Agentes IA"])

# Nota: Las rutas modulares estarán disponibles luego de crear sus respectivos archivos en /routers/
