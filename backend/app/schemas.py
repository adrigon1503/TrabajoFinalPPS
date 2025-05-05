from pydantic import BaseModel, EmailStr
from typing import Optional

# ==== Partido ====

class PartidoCreate(BaseModel):
    equipo_local: str
    equipo_visitante: str
    goles_local: int
    goles_visitante: int

class PartidoOut(PartidoCreate):
    id: int

    class Config:
        from_attributes = True

# ==== Usuario ====

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    twofa_enabled: bool
    is_admin: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class TwoFAVerify(BaseModel):
    username: str
    token: str
