import os

import requests

TEST_USER = os.getenv("TEST_USER")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")


def test_login_sucesso(base_url):
    """Valida o login com credenciais corretas e o retorno do token JWT."""
    print(f"\n[TEST_AUTH] Testando /api/login para o usuário: '{TEST_USER}'")
    payload = {"username": TEST_USER, "password": TEST_PASSWORD}

    response = requests.post(f"{base_url}/api/login", json=payload)

    assert response.status_code == 200, "O status code deve ser 200 OK"
    data = response.json()
    assert "access_token" in data, "A resposta deve conter um access_token"
    assert data["token_type"] == "bearer", "O tipo de token deve ser bearer"


def test_login_credenciais_invalidas(base_url):
    """Valida a recusa de autenticação para senha incorreta (HTTP 400)."""
    payload = {"username": TEST_USER, "password": "senha_invalida_xyz"}

    response = requests.post(f"{base_url}/api/login", json=payload)

    assert response.status_code == 400, "O status code deve ser 400"
    assert response.json()["detail"] == "Usuário ou senha incorretos"
