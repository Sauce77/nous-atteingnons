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
pip install -r requirements.txt

echo "Iniciando la aplicacion..."
echo "Puedes acceder desde tu navegador en: http://localhost:8000"
echo "Presiona CTRL+C para detener el servidor."

# Inicia el servidor Waitress
waitress-serve --host=0.0.0.0 --port=8000 buscador.wsgi:application