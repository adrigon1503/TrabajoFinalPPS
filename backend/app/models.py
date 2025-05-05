from sqlalchemy import Column, Integer, String, DateTime, Boolean
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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    twofa_secret = Column(String, nullable=True)
    twofa_enabled = Column(Boolean, default=False)
