from pydantic import BaseModel

class PartidoCreate(BaseModel):
    equipo_local: str
    equipo_visitante: str
    goles_local: int
    goles_visitante: int

class PartidoOut(PartidoCreate):
    id: int

    class Config:
        orm_mode = True
