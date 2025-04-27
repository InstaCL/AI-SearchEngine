#!/bin/bash

echo "📡 Iniciando servidor en el puerto 10000"

# Definir el directorio base para que Python encuentre los paquetes
export PYTHONPATH="$PYTHONPATH:$(pwd)/backend"

# Mostrar advertencia si faltan claves
if [[ -z "$OPENAI_API_KEY" || -z "$PINECONE_API_KEY" ]]; then
  echo "⚠️ Advertencia: Algunas variables de entorno están vacías. Verifica tu archivo .env o configuración en Render."
else
  echo "✅ Variables de entorno cargadas correctamente"
fi

# Lanzar el servidor Uvicorn apuntando al main.py dentro de /backend
uvicorn main:app --host 0.0.0.0 --port 10000 --reload
