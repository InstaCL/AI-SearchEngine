#!/bin/bash
echo "📡 Iniciando servidor en el puerto $PORT"
uvicorn api.main:app --host 0.0.0.0 --port $PORT
