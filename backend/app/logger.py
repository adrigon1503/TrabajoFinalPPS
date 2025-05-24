import logging
import os

# Aseguramos que la carpeta de logs exista
os.makedirs("logs", exist_ok=True)

# Configuración de logger
logger = logging.getLogger("backend_logger")
logger.setLevel(logging.DEBUG)  # Captura todos los niveles

# Formato común
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Handler para archivo
file_handler = logging.FileHandler("logs/backend.log")
file_handler.setFormatter(formatter)

# Handler para consola (opcional)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Evitar múltiples handlers duplicados
if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Exportar logger
def get_logger():
    return logger
