import os
import io
import qrcode
import pyotp
from jose import JWTError, jwt
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import engine, SessionLocal
from backend.app.logger import get_logger
from backend.auth.routers import router as auth_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(auth_router, prefix="/auth")


logger = get_logger()

logger.info("Backend iniciado")
logger.warning("Advertencia de ejemplo")
logger.error("Error de ejemplo")

# Cargar variables de entorno
load_dotenv(".env")

# Configuración JWT
SECRET_KEY = os.getenv("SECRET_KEY", "clave_insegura_dev")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Crear tablas si no existen
models.Base.metadata.create_all(bind=engine)

# Crear app FastAPI
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependencia de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener el usuario actual a partir del token
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# ====== ENDPOINTS ======

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Waterpolo Match Registration creada por AAR"}

# --------- PARTIDOS ---------

@app.get("/partidos/", response_model=list[schemas.PartidoOut])
def listar_partidos(db: Session = Depends(get_db)):
    return crud.get_partidos(db)

@app.post("/partidos/", response_model=schemas.PartidoOut)
def crear_partido(partido: schemas.PartidoCreate, db: Session = Depends(get_db)):
    return crud.create_partido(db, partido.dict())

# --------- USUARIOS ---------

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    return crud.create_user(db, user.username, user.email, user.password)

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Usuario inactivo")
    token_data = {"sub": user.username}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/enable-2fa/")
def enable_2fa(current_user: schemas.UserLogin, db: Session = Depends(get_db)):
    secret = crud.enable_2fa_for_user(db, current_user.username)
    if not secret:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=current_user.username, issuer_name="WaterpoloAPI")
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.post("/verify-2fa/")
def verify_2fa(verify: schemas.TwoFAVerify, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, verify.username)
    if not user or not user.twofa_enabled:
        raise HTTPException(status_code=400, detail="2FA no habilitado o usuario no encontrado")
    if crud.verify_2fa_token(user, verify.token):
        return {"message": "2FA verificado correctamente"}
    else:
        raise HTTPException(status_code=401, detail="Código 2FA inválido")

# --------- ADMIN ---------

@app.post("/admin/create-user", response_model=schemas.UserOut)
def admin_create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    return crud.create_user(db, user.username, user.email, user.password, is_admin=True)
