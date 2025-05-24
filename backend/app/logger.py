import os
import logging

# Definir la ruta del archivo de log
LOG_DIR = "logs"
LOG_FILE = "backend.log"
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Crear el directorio de logs si no existe
os.makedirs(LOG_DIR, exist_ok=True)

# Si existe un directorio en lugar de archivo, eliminarlo
if os.path.isdir(LOG_PATH):
    os.rmdir(LOG_PATH)

# Crear un archivo de log vacío si no existe
if not os.path.exists(LOG_PATH):
    with open(LOG_PATH, 'w'):
        pass

# Configuración del logger
logger = logging.getLogger("backend")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_PATH)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Evitar agregar múltiples handlers en recargas (útil para entornos interactivos o tests)
if not logger.handlers:
    logger.addHandler(file_handler)

def get_logger():
    return logger
