@echo off
echo "Configurando el entorno por primera vez. Esto puede tardar unos minutos..."

:: Revisa si el entorno virtual existe, si no, lo crea.
if not exist venv (
    echo "Creando entorno virtual..."
    python -m venv venv
)

echo "Instalando/actualizando dependencias..."
:: Instala las dependencias desde requirements.txt
call venv\Scripts\pip.exe install -r requirements.txt

echo "Iniciando la aplicacion..."
echo "Puedes acceder desde tu navegador en: http://localhost:8000"
echo "Presiona CTRL+C para detener el servidor."

:: Inicia el servidor Waitress
call venv\Scripts\waitress-serve.exe --host=0.0.0.0 --port=8000 buscador.wsgi:application