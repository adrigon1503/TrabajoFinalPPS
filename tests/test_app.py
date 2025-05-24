from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_register_and_login():
    username = "usuario_test"
    password = "password123"
    email = "usuario@test.com"

    # Intentar registrar
    response = client.post("/auth/register", json={
        "username": username,
        "password": password,
        "email": email
    })

    assert response.status_code in (200, 400)  # Puede ya existir el usuario
    if response.status_code == 400:
        assert response.json()["detail"] == "El usuario ya existe"

    # Login
    response = client.post("/auth/login", data={
        "username": username,
        "password": password
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Token funcional
    token = data["access_token"]

    # Obtener lista de partidos autenticado
    response = client.get("/partidos/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
