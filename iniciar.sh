#!/bin/bash
echo "Configurando el entorno por primera vez. Esto puede tardar unos minutos..."

# Revisa si el entorno virtual existe, si no, lo crea.
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

echo "Activando entorno e instalando dependencias..."
# Activa el entorno virtual e instala los paquetes
source venv/bin/activate
pip install -r requirements.txt > /dev/null

echo "Recolectando archivos estaticos..."
python3 manage.py collectstatic --noinput > /dev/null

echo "Iniciando el servidor en segundo plano..."

# 1. Inicia el servidor Waitress en segundo plano usando '&'
nohup waitress-serve --host=127.0.0.1 --port=8000 buscador.wsgi:application &

echo "Esperando a que el servidor arranque (5 segundos)..."

# 2. Espera 5 segundos para dar tiempo a que el servidor se inicie.
sleep 5

echo "Abriendo la aplicacion en tu navegador..."

# 3. Abre el navegador web. 'xdg-open' en Linux, 'open' en macOS.
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open http://127.0.0.1:8000
elif [[ "$OSTYPE" == "darwin"* ]]; then
    open http://127.0.0.1:8000
fi

echo ""
echo "Listo! El servidor se esta ejecutando en segundo plano."
echo "Para detenerlo, busca el proceso con 'ps aux | grep waitress' y usa 'kill <PID>'."