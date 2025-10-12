FROM python:3.11-slim

WORKDIR /app

# 🔹 Instalar certificados CA y dependencias SSL
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates gnupg && \
    update-ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 🔹 Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn flake8 pytest pymongo

# 🔹 Copiar el resto del proyecto
COPY . .

# 🔹 Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# 🔹 Exponer puerto
EXPOSE 5000

# 🔹 Comando de inicio (Gunicorn para producción)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "3", "--threads", "2"]
