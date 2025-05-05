#!/bin/bash

echo "📡 Iniciando servidor en el puerto 10000"

# Ruta absoluta al backend
export PYTHONPATH=$(pwd)/instacommerce-ai/backend

echo "✅ Variables de entorno cargadas correctamente"

uvicorn api.main:app --host 0.0.0.0 --port 10000
