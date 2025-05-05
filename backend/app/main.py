from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, SessionLocal
from dotenv import load_dotenv
import secrets
import os

# Cargar variables de entorno
load_dotenv()

# Leer credenciales de entorno
USER = os.getenv("BASIC_AUTH_USER")
PASS = os.getenv("BASIC_AUTH_PASS")

# Crear tablas
models.Base.metadata.create_all(bind=engine)

# Configuración de la aplicación
app = FastAPI(
    title="API Waterpolo",
    description="Registro de partidos",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

# Seguridad básica
security = HTTPBasic()

def autenticacion_basica(credentials: HTTPBasicCredentials = Depends(security)):
    usuario_correcto = secrets.compare_digest(credentials.username, USER)
    password_correcto = secrets.compare_digest(credentials.password, PASS)
    if not (usuario_correcto and password_correcto):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )

# Documentación protegida
@app.get("/docs", include_in_schema=False)
def custom_swagger_ui(credentials: HTTPBasicCredentials = Depends(autenticacion_basica)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Waterpolo")

@app.get("/openapi.json", include_in_schema=False)
def custom_openapi(credentials: HTTPBasicCredentials = Depends(autenticacion_basica)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)

# Conexión a la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Waterpolo Match Registration creada por AAR"}

@app.get("/partidos/", response_model=list[schemas.PartidoOut])
def listar_partidos(db: Session = Depends(get_db)):
    return db.query(models.Partido).all()

@app.post("/partidos/", response_model=schemas.PartidoOut)
def crear_partido(partido: schemas.PartidoCreate, db: Session = Depends(get_db)):
    nuevo = models.Partido(**partido.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
