from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Waterpolo",
    description="Registro de partidos",
    version="1.0.0",
    docs_url="/docs",            # Swagger UI
    redoc_url="/redoc",          # Documentación alternativa (opcional)
    openapi_url="/openapi.json"  # JSON del schema OpenAPI
)

# Obtener conexión a la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Waterpolo Match Registration creada por AAR"}

# Endpoint para listar partidos
@app.get("/partidos/", response_model=list[schemas.PartidoOut])
def listar_partidos(db: Session = Depends(get_db)):
    return db.query(models.Partido).all()

# Endpoint para crear partidos
@app.post("/partidos/", response_model=schemas.PartidoOut)
def crear_partido(partido: schemas.PartidoCreate, db: Session = Depends(get_db)):
    nuevo = models.Partido(**partido.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo