@echo off
cd /d %~dp0
title Lanzador de Aplicacion Django

echo Verificando instalacion de Python...
:: Verifica si el lanzador de Python existe
py -3 --version 2>nul
if %errorlevel% neq 0 (
    echo ERROR: No se encontro Python.
    echo Por favor, instalalo desde python.org y asegurate de marcar "Add Python to PATH".
    pause
    exit /b
)

echo Configurando el entorno por primera vez. Esto puede tardar unos minutos...

:: Usa 'py -3' para crear el venv
if not exist venv (
    echo Creando entorno virtual...
    py -3 -m venv venv
)

echo.
echo =================================================================
echo  INSTALANDO DEPENDENCIAS (POR FAVOR, REVISA SI HAY ERRORES AQUI)
echo =================================================================
echo.

:: Quitamos '> nul' para ver la salida completa de pip
call venv\Scripts\pip.exe install -r requirements.txt

echo.
echo =================================================================
echo.

echo Recolectando archivos estaticos...
:: Usa el python.exe del venv para ejecutar manage.py
call venv\Scripts\python.exe manage.py collectstatic --noinput > nul

echo.
echo Iniciando el servidor en una nueva ventana...
start "Servidor Django" call venv\Scripts\waitress-serve.exe --host=127.0.0.1 --port=8000 buscador.wsgi:application

echo Esperando a que el servidor arranque (5 segundos)...
timeout /t 5 /nobreak > nul

echo Abriendo la aplicacion en tu navegador...
start http://127.0.0.1:8000

echo.
echo Listo! El servidor se esta ejecutando en una ventana separada.
echo Puedes cerrar esta ventana.
pause
