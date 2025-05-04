from sqlalchemy.orm import Session
from . import models

def create_match(db: Session, match_data):
    db_match = models.Match(**match_data)
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

def get_matches(db: Session):
    return db.query(models.Match).all()
