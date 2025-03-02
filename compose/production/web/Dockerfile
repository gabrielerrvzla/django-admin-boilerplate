# Usa una versión estable y ligera de Python
FROM python:3.13.2-slim

# Establece el directorio de trabajo
WORKDIR /app

# Configura variables de entorno para optimizar el rendimiento
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instala dependencias del sistema necesarias para Django y PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia y instala las dependencias de Python antes del código fuente para mejorar la caché de Docker
COPY ./requirements /requirements
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /requirements/production.txt

# Copia la aplicación Django al contenedor
COPY src /app

# Configura el usuario no root para mayor seguridad
RUN groupadd -r django && useradd -r -g django django

# Crea y asigna permisos al directorio de archivos estáticos antes de cambiar de usuario
RUN mkdir -p /app/staticfiles && chown -R django:django /app/staticfiles

# Cambia al usuario seguro
USER django