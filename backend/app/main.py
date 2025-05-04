# backend/app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database, crud

from pydantic import BaseModel

app = FastAPI()

# Crear las tablas al iniciar
models.Base.metadata.create_all(bind=database.engine)

# Dependencia para obtener sesión de BD
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MatchCreate(BaseModel):
    team_home: str
    team_away: str
    score_home: int
    score_away: int

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Waterpolo"}

@app.post("/partidos/")
def create_match(match: MatchCreate, db: Session = Depends(get_db)):
    return crud.create_match(db, match.dict())

@app.get("/partidos/")
def list_matches(db: Session = Depends(get_db)):
    return crud.get_matches(db)
