#!/bin/bash

echo "📡 Iniciando servidor en el puerto 10000"

# Establece la ruta de módulos
export PYTHONPATH=$(pwd)/instacommerce-ai

echo "✅ Variables de entorno cargadas correctamente"

# Cambia al directorio del backend (nivel donde está api/)
cd instacommerce-ai

# Ejecuta el servidor apuntando a api.main:app
uvicorn api.main:app --host 0.0.0.0 --port 10000
