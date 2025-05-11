import sys
import os
import pytest
from fastapi.testclient import TestClient

# Agregar el directorio raíz del proyecto al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Importar la aplicación desde backend
from backend.app.main import app  
from backend.app.database import SessionLocal
from backend.app import crud, schemas
import json

# Crear un cliente de pruebas para FastAPI
client = TestClient(app)

# 1. Prueba de registro de usuario
def test_register_user():
    response = client.post("/auth/register", json={
        "email": "testuser@example.com",
        "password": "testpassword123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data  # Verifica que se devuelve un JWT

# 2. Prueba de login de usuario
def test_login_user():
    response = client.post("/auth/register", json={
        "email": "testlogin@example.com",
        "password": "testpassword123"
    })
    assert response.status_code == 200
    data = response.json()
    access_token = data["access_token"]

    # Usar el token para hacer login
    response = client.post("/auth/login", data={
        "username": "testlogin@example.com",
        "password": "testpassword123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == access_token

# 3. Prueba de 2FA (verificación)
def test_2fa_verification():
    # Primero, creamos un usuario con 2FA habilitado
    response = client.post("/auth/register", json={
        "email": "test2fa@example.com",
        "password": "testpassword123",
        "twofa_enabled": True
    })
    assert response.status_code == 200

    # Verificamos que se recibe el código de 2FA (en un entorno real, deberíamos simularlo)
    response = client.post("/auth/verify-2fa", json={
        "email": "test2fa@example.com",
        "code": "123456"  # Código de ejemplo
    })
    assert response.status_code == 200  # Si el código es correcto

# 4. Crear un partido
def test_create_partido():
    access_token = "your_jwt_token_here"  # Obtén un token válido antes

    response = client.post("/partidos/", json={
        "equipo_local": "Equipo A",
        "equipo_visitante": "Equipo B",
        "fecha": "2025-05-11",
        "resultado_local": 10,
        "resultado_visitante": 8
    }, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["equipo_local"] == "Equipo A"
    assert data["equipo_visitante"] == "Equipo B"

# 5. Obtener partidos
def test_get_partidos():
    response = client.get("/partidos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Verifica que se devuelve una lista de partidos

# 6. Actualizar partido
def test_update_partido():
    # Primero, crea un partido
    response = client.post("/partidos/", json={
        "equipo_local": "Equipo C",
        "equipo_visitante": "Equipo D",
        "fecha": "2025-05-11",
        "resultado_local": 7,
        "resultado_visitante": 6
    })
    partido_id = response.json()["id"]

    # Ahora, actualiza el partido
    response = client.put(f"/partidos/{partido_id}", json={
        "equipo_local": "Equipo C",
        "equipo_visitante": "Equipo D",
        "fecha": "2025-05-11",
        "resultado_local": 8,
        "resultado_visitante": 6
    })
    assert response.status_code == 200
    data = response.json()
    assert data["resultado_local"] == 8

# 7. Eliminar partido
def test_delete_partido():
    # Primero, crea un partido
    response = client.post("/partidos/", json={
        "equipo_local": "Equipo E",
        "equipo_visitante": "Equipo F",
        "fecha": "2025-05-11",
        "resultado_local": 9,
        "resultado_visitante": 7
    })
    partido_id = response.json()["id"]

    # Ahora, elimina el partido
    response = client.delete(f"/partidos/{partido_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Partido eliminado exitosamente"}

# 8. Verificar acceso restringido (ejemplo para admin)
def test_admin_restricted_access():
    # Intentar crear un partido sin estar autenticado
    response = client.post("/partidos/", json={
        "equipo_local": "Equipo G",
        "equipo_visitante": "Equipo H",
        "fecha": "2025-05-11",
        "resultado_local": 10,
        "resultado_visitante": 9
    })
    assert response.status_code == 401  # Debe fallar por no estar autenticado

# 9. Prueba de administrador (habilitar y deshabilitar usuario)
def test_admin_user_management():
    # Suponiendo que ya tienes un administrador logueado
    admin_token = "admin_jwt_token_here"  # Obtén el token de administrador

    response = client.patch("/admin/deactivate_user", json={
        "user_id": 1  # ID de un usuario para deshabilitar
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Usuario deshabilitado correctamente"
