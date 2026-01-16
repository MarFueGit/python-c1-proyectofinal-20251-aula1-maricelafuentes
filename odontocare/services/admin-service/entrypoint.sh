#!/bin/sh
set -e

echo "Inicializando base de datos..."
python init_db.py

echo "Creando admin inicial..."
python create_admin.py

echo "Levantando servidor..."
python run.py &

SERVER_PID=$!

echo "Esperando a que el servidor esté listo..."

python - << 'EOF'
import time
import urllib.request

url = "http://localhost:5000/health"

while True:
    try:
        urllib.request.urlopen(url, timeout=1)
        break
    except Exception:
        time.sleep(1)

print("Servidor listo!")
EOF

echo "Corriendo carga inicial..."
python carga_inicial.py

echo "Servidor en ejecución"
wait $SERVER_PID