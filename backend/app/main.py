from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Obtener conexión a la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Waterpolo"}

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