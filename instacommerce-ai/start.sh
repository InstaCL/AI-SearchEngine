#!/bin/bash

echo "📡 Iniciando servidor en el puerto 10000"

# Establece el directorio raíz como PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)/instacommerce-ai/backend

echo "✅ Variables de entorno cargadas correctamente"

# Ejecuta Uvicorn desde la ruta correcta
uvicorn main:app --host 0.0.0.0 --port 10000
