
import requests


def test_listar_ativos_publicos(base_url):
    """Verifica se a API consegue listar os ativos."""
    response = requests.get(f"{base_url}/api/assets")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_atualizar_taxa_ativo(base_url, auth_headers):
    """Verifica se a API consegue atualizar a taxa de um ativo."""
    payload = {
        "id": 1,
        "asset_name": "Ativo Teste Atualizacao",  # Nome do ativo
        "annual_rate": 11.75,  # Taxa anual do ativo
    }

    response = requests.put(
        f"{base_url}/api/assets",
        json=payload,
        headers=auth_headers,
    )

    print(response.json())

    assert response.status_code == 200
