#!/bin/bash

echo "📡 Iniciando servidor en el puerto 10000"

# Asegurar que Python pueda encontrar los paquetes del backend
export PYTHONPATH="$PYTHONPATH:$(pwd)/backend"

# Verificación de variables de entorno necesarias
if [[ -z "$OPENAI_API_KEY" || -z "$PINECONE_API_KEY" ]]; then
  echo "⚠️ Advertencia: Variables de entorno faltantes. Revisa la configuración de Render o el archivo .env"
else
  echo "✅ Variables de entorno cargadas correctamente"
fi

# Lanzar el servidor FastAPI usando Uvicorn
uvicorn backend.main:app --host 0.0.0.0 --port 10000
