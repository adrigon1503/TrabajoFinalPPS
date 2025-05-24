FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar e instalar dependencias
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación y los tests
COPY backend /app/backend
COPY tests /app/tests

# Añadir PYTHONPATH para que funcione el import desde tests/
ENV PYTHONPATH=/app

# Comando por defecto para producción
CMD ["gunicorn", "backend.app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
