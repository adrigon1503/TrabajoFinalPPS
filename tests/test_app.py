import sys
import os
import pytest
from fastapi.testclient import TestClient

# Agregar el directorio raíz del proyecto al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from backend.app.main import app
from backend.app.database import SessionLocal
from backend.app import crud, schemas

client = TestClient(app)

# Helpers
def register_user(email, password, twofa_enabled=False):
    response = client.post("/auth/register", json={
        "email": email,
        "password": password,
        "twofa_enabled": twofa_enabled
    })
    assert response.status_code == 200
    return response.json()["access_token"]

def login_user(email, password):
    response = client.post("/auth/login", data={
        "username": email,
        "password": password
    })
    assert response.status_code == 200
    return response.json()["access_token"]

def get_token(email, password, twofa_enabled=False):
    try:
        return register_user(email, password, twofa_enabled)
    except:
        return login_user(email, password)

# 1. Prueba de registro de usuario
def test_register_user():
    token = register_user("testuser@example.com", "testpassword123")
    assert token is not None

# 2. Prueba de login de usuario
def test_login_user():
    email = "testlogin@example.com"
    password = "testpassword123"
    register_user(email, password)
    token = login_user(email, password)
    assert token is not None

# 3. Prueba de 2FA (verificación)
def test_2fa_verification():
    email = "test2fa@example.com"
    password = "testpassword123"
    register_user(email, password, twofa_enabled=True)

    response = client.post("/auth/verify-2fa", json={
        "email": email,
        "code": "123456"  # Código de ejemplo
    })
    assert response.status_code == 200

# 4. Crear un partido
def test_create_partido():
    token = get_token("creator@example.com", "securepass123")
    response = client.post("/partidos/", json={
        "equipo_local": "Equipo A",
        "equipo_visitante": "Equipo B",
        "fecha": "2025-05-11",
        "resultado_local": 10,
        "resultado_visitante": 8
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201
    data = response.json()
    assert "id" in data

# 5. Obtener partidos
def test_get_partidos():
    response = client.get("/partidos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# 6. Actualizar partido
def test_update_partido():
    token = get_token("updater@example.com", "updatepass123")
    # Crear partido
    response = client.post("/partidos/", json={
        "equipo_local": "Equipo C",
        "equipo_visitante": "Equipo D",
        "fecha": "2025-05-11",
        "resultado_local": 7,
        "resultado_visitante": 6
    }, headers={"Authorization": f"Bearer {token}"})
    partido_id = response.json()["id"]

    # Actualizar partido
    response = client.put(f"/partidos/{partido_id}", json={
        "equipo_local": "Equipo C",
        "equipo_visitante": "Equipo D",
        "fecha": "2025-05-11",
        "resultado_local": 8,
        "resultado_visitante": 6
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["resultado_local"] == 8

# 7. Eliminar partido
def test_delete_partido():
    token = get_token("deleter@example.com", "deletepass123")
    # Crear partido
    response = client.post("/partidos/", json={
        "equipo_local": "Equipo E",
        "equipo_visitante": "Equipo F",
        "fecha": "2025-05-11",
        "resultado_local": 9,
        "resultado_visitante": 7
    }, headers={"Authorization": f"Bearer {token}"})
    partido_id = response.json()["id"]

    # Eliminar partido
    response = client.delete(f"/partidos/{partido_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Partido eliminado exitosamente"}

# 8. Verificar acceso restringido sin login
def test_admin_restricted_access():
    response = client.post("/partidos/", json={
        "equipo_local": "Equipo G",
        "equipo_visitante": "Equipo H",
        "fecha": "2025-05-11",
        "resultado_local": 10,
        "resultado_visitante": 9
    })
    assert response.status_code == 401

# 9. Prueba de administrador (habilitar y deshabilitar usuario)
def test_admin_user_management():
    admin_token = get_token("admin@example.com", "adminpass123")
    # Aquí podrías registrar previamente al usuario con ID 1 si tu base parte vacía
    response = client.patch("/admin/deactivate_user", json={
        "user_id": 1
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Usuario deshabilitado correctamente"
