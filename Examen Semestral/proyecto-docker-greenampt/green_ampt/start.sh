#!/bin/bash
set -e

echo "Iniciando API interna (Bisección / Falsa Posición) en :8001..."
uvicorn main:app --host 127.0.0.1 --port 8001 &

sleep 2

echo "Iniciando Green-Ampt (Reflex) en :3000..."
exec reflex run --env prod --backend-host 0.0.0.0
