# backend/app/models.py
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
import datetime

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    team_home = Column(String, nullable=False)
    team_away = Column(String, nullable=False)
    score_home = Column(Integer, default=0)
    score_away = Column(Integer, default=0)
    date = Column(DateTime, default=datetime.datetime.utcnow)
