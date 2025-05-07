#!/bin/bash

echo "📡 Iniciando servidor en el puerto 10000"
echo "✅ Variables de entorno cargadas correctamente"

# Asegura que este sea el directorio actual
export PYTHONPATH=$PYTHONPATH:$(pwd)

uvicorn api.main:app --host 0.0.0.0 --port 10000