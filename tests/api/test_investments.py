

import requests


def test_listar_investimentos(base_url, auth_headers):
    """Testa a listagem de investimentos do usuário."""
    response = requests.get(
        f"{base_url}/api/investments",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)



def test_excluir_investimento(base_url, auth_headers):
    """Testa a exclusao de um investimento criado para teste."""

    # Cria um investimento temporario
    payload = {
        "asset_name": "CDB",
        "amount": 1000.00,
        "purchase_price": 1.00,
        "days_invested": 30,
        "planned_days": 365
    }

    criacao = requests.post(
        f"{base_url}/api/investments",
        json=payload,
        headers=auth_headers
    )

    assert criacao.status_code == 201

    # Guarda o ID do investimento criado
    investimento_id = criacao.json()["id"]

    # Exclui somente o investimento criado acima
    resposta = requests.delete(
        f"{base_url}/api/investments/{investimento_id}",
        headers=auth_headers
    )

    assert resposta.status_code == 200
