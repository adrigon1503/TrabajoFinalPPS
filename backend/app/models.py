from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
import datetime

class Partido(Base):
    __tablename__ = "partidos"

    id = Column(Integer, primary_key=True, index=True)
    equipo_local = Column(String, nullable=False)
    equipo_visitante = Column(String, nullable=False)
    goles_local = Column(Integer, default=0)
    goles_visitante = Column(Integer, default=0)
    date = Column(DateTime, default=datetime.datetime.utcnow)
