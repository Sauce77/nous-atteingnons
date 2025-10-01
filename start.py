import os

# Esto puede mitigar problemas de concurrencia y rastreo de CPU en entornos virtualizados.
os.environ['OMP_NUM_THREADS'] = '1' 
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

import sys
from django.core.management import execute_from_command_line
import webbrowser
import threading
import time
import traceback

# --- 1. CONFIGURACIÓN DEL ENTORNO ---
# Establece la configuración de Django
# Reemplaza 'mi_proyecto.settings' con la ruta real a tu settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'buscador.settings')

# Define el puerto y la dirección
HOST = '127.0.0.1'
PORT = '8000'
URL = f'http://{HOST}:{PORT}'

def run_django_server():
    """Inicia el servidor de desarrollo de Django."""
    
    # El argumento '--noreload' es crucial para evitar errores con PyInstaller.
    # El argumento '--nothreading' puede ser necesario si experimentas problemas
    # de concurrencia en el ejecutable.
    try:
        # Usa el comando runserver con la dirección y el puerto especificados
        print(f"Iniciando servidor Django en {URL}...")
        execute_from_command_line([
            sys.argv[0],  # El nombre del script/ejecutable
            'runserver',
            f'{HOST}:{PORT}',
            '--noreload',
            '--nothreading',
        ])
    except Exception as e:
        print("\n--- ERROR CRÍTICO ---")
        traceback.print_exc() # Muestra la traza completa
        input("\nPresiona ENTER para cerrar la ventana...") # Mantiene la ventana abierta
        sys.exit(1)

def open_browser_delay():
    """Espera un momento para asegurar que el servidor esté activo antes de abrir el navegador."""
    time.sleep(3) # Espera 3 segundos
    try:
        webbrowser.open_new_tab(URL)
        print(f"Abriendo la aplicación en el navegador: {URL}")
    except Exception as e:
        print(f"No se pudo abrir el navegador. Por favor, abre manualmente: {URL}")

if __name__ == '__main__':
    # Ejecutar el servidor en un hilo separado
    server_thread = threading.Thread(target=run_django_server)
    server_thread.daemon = True # Permite que el hilo muera cuando el programa principal termine
    server_thread.start()

    # Abrir el navegador en otro hilo después de un breve retraso
    browser_thread = threading.Thread(target=open_browser_delay)
    browser_thread.start()

    # Mantener el hilo principal activo. Esto es para que la aplicación
    # no termine inmediatamente.
    print("La aplicación se está ejecutando. Cierra la ventana de la consola para detenerla.")
    
    # Una forma simple de mantener el hilo principal vivo mientras el servidor se ejecuta
    # se podría usar un bucle infinito o una entrada simple
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Aplicación detenida por el usuario.")
    except SystemExit:
        # Esto captura la salida cuando se cierra la ventana de la consola
        print("Aplicación cerrada.")