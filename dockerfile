# Usa una imagen base de Python (ajusta la versión)
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos e instálalos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instala Gunicorn o uWSGI (necesario para producción/standalone)
RUN pip install gunicorn

# Copia el resto de tu código Django
COPY . .

# Recolecta archivos estáticos (asegúrate de que STATIC_ROOT esté configurado en settings.py)
RUN python manage.py collectstatic --no-input

# Expone el puerto por defecto de Django
EXPOSE 8000

# Comando para correr el servidor Gunicorn
# 'mi_proyecto.wsgi:application' debe coincidir con la ruta de tu archivo wsgi
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mi_proyecto.wsgi:application"]