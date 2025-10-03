@echo off
title Lanzador de Aplicacion Django

echo Configurando el entorno por primera vez. Esto puede tardar unos minutos...

:: Revisa si el entorno virtual existe, si no, lo crea.
if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
)

echo Instalando/actualizando dependencias (esto puede tardar)...
:: Se oculta la salida de pip para una pantalla mas limpia
call venv\Scripts\pip.exe install -r requirements.txt > nul

echo Recolectando archivos estaticos...
:: Se oculta la salida de collectstatic
call venv\Scripts\python.exe manage.py collectstatic --noinput > nul

echo.
echo Iniciando el servidor en una nueva ventana...

:: 1. Inicia el servidor en una nueva ventana para no bloquear este script.
start "Servidor Django" call venv\Scripts\waitress-serve.exe --host=127.0.0.1 --port=8000 buscador.wsgi:application

echo Esperando a que el servidor arranque (5 segundos)...

:: 2. Espera 5 segundos para dar tiempo a que el servidor se inicie.
timeout /t 5 /nobreak > nul

echo Abriendo la aplicacion en tu navegador...

:: 3. Abre el navegador web en la direccion correcta.
start http://127.0.0.1:8000

echo.
echo Listo! El servidor se esta ejecutando en una ventana separada.
echo Puedes cerrar esta ventana.
pause