from sqlalchemy.orm import Session
from . import models, schemas
import pyotp
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------- PARTIDOS --------------------

def create_partido(db: Session, partido_data: schemas.PartidoCreate):
    db_partido = models.Partido(**partido_data.dict())
    db.add(db_partido)
    db.commit()
    db.refresh(db_partido)
    return db_partido

def get_partidos(db: Session):
    return db.query(models.Partido).all()

# -------------------- USUARIOS --------------------

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, username: str, email: str, password: str, is_admin: bool = False):
    hashed_pw = pwd_context.hash(password)
    db_user = models.User(
        username=username,
        email=email,
        hashed_password=hashed_pw,
        is_admin=is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def enable_2fa_for_user(db: Session, username: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    secret = pyotp.random_base32()
    user.twofa_secret = secret
    user.twofa_enabled = True
    db.commit()
    db.refresh(user)
    return secret

def verify_2fa_token(user: models.User, token: str):
    if not user.twofa_secret:
        return False
    totp = pyotp.TOTP(user.twofa_secret)
    return totp.verify(token)

def set_user_active_status(db: Session, username: str, active: bool):
    user = get_user_by_username(db, username)
    if not user:
        return None
    user.is_active = active
    db.commit()
    db.refresh(user)
    return user