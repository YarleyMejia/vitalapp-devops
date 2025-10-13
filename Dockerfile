FROM python:3.11-slim

WORKDIR /app

# Instalar certificados raíz del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    update-ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn flake8 pytest pymongo

# Copiar el proyecto
COPY . .

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

EXPOSE 5000

# Comando de inicio
CMD exec gunicorn --bind 0.0.0.0:${PORT:-5000} app:app --workers 3 --threads 2

