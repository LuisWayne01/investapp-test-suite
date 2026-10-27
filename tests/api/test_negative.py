import requests


def test_login_credenciais_invalidas(base_url):
    """Verifica se o login rejeita credenciais incorretas."""

    payload = {
        "username": "usuario_inexistente_teste",
        "password": "senha_incorreta_teste"
    }

    response = requests.post(
        f"{base_url}/api/login",
        json=payload
    )

    assert response.status_code == 400


def test_listar_investimentos_sem_autenticacao(base_url):
    """Verifica se a API rejeita uma consulta sem autenticação."""

    response = requests.get(
        f"{base_url}/api/investments"
    )

    assert response.status_code == 401


def test_criar_investimento_payload_invalido(
    base_url,
    auth_headers
):
    """Verifica se a API rejeita um payload sem os campos obrigatórios."""

    payload = {}

    response = requests.post(
        f"{base_url}/api/investments",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 422