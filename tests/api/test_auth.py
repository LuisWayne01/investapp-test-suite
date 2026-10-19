import os
import requests

BASE_URL = os.getenv("API_BASE_URL", "https://5bm1nctd1f.execute-api.us-east-1.amazonaws.com")

def test_login_sucesso():
    """Valida o login com credenciais corretas lidas do .env"""
    payload = {
        "username": os.getenv("TEST_USER"),
        "password": os.getenv("TEST_PASSWORD")
    }
    
    response = requests.post(f"{BASE_URL}/api/login", json=payload)
    
    assert response.status_code == 200, "O status code deve ser 200 OK"
    data = response.json()
    assert "access_token" in data, "A resposta deve conter um access_token"
    assert data["token_type"] == "bearer", "O tipo de token deve ser bearer"

def test_login_credenciais_invalidas():
    """Valida a recusa de login ao informar senha incorreta"""
    payload = {
        "username": "usuario_invalido",
        "password": "senha_errada"
    }
    
    response = requests.post(f"{BASE_URL}/api/login", json=payload)
    
    # Adicione esta linha para converter a resposta da API em um dicionário Python:
    data = response.json()
    
    assert response.status_code == 400, "O status code deve ser 400 Bad Request"
    assert data["detail"] == "Usuário ou senha incorretos", "A mensagem de erro deve ser exata"