FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar correctamente la carpeta backend y tests al contenedor
COPY backend /app/backend
COPY tests /app/tests

# Añadir PYTHONPATH para que funcione el import desde tests/
ENV PYTHONPATH=/app

# Comando por defecto para producción (puedes cambiar esto en desarrollo o tests)
CMD ["gunicorn", "backend.app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
