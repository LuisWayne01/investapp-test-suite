import csv
from pathlib import Path

import pytest
import requests


def test_criar_investimento_valido(base_url, auth_headers):
    """Valida a criação de um investimento com dados válidos."""

    payload = {
        "asset_name": "CDB",
        "amount": 1500.00,
        "purchase_price": 1.00,
        "days_invested": 30,
        "planned_days": 365,
    }

    response = requests.post(
        f"{base_url}/api/investments",
        json=payload,
        headers=auth_headers,
        timeout=15,
    )

    assert response.status_code == 201, (
        f"Esperado HTTP 201, mas a API retornou "
        f"{response.status_code}: {response.text}"
    )

    data = response.json()

    assert isinstance(data, dict)
    assert data["asset_name"] == payload["asset_name"]
    assert float(data["amount"]) == payload["amount"]
    assert float(data["purchase_price"]) == payload["purchase_price"]
    assert data["days_invested"] == payload["days_invested"]
    assert data["planned_days"] == payload["planned_days"]

    # Limpeza: remove o investimento criado para não acumular dados
    requests.delete(
        f"{base_url}/api/investments/{data['id']}",
        headers=auth_headers,
        timeout=15,
    )


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


def carregar_dados_investimentos_csv():
    """Le dinamicamente o arquivo CSV em tests/data/dados_investimentos.csv."""
    caminho_csv = (
        Path(__file__).resolve().parent.parent / "data" / "dados_investimentos.csv"
    )

    if not caminho_csv.exists():
        raise FileNotFoundError(
            f"Arquivo de massa CSV nao encontrado em: {caminho_csv}"
        )

    casos = []
    with open(caminho_csv, mode="r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            casos.append(
                (
                    linha["asset_name"],
                    float(linha["amount"]),
                    float(linha["purchase_price"]),
                    int(linha["days_invested"]),
                    int(linha["planned_days"]),
                    int(linha["status_esperado"]),
                )
            )
    return casos


@pytest.mark.parametrize(
    "asset, amount, price, days, planned, status_esperado",
    carregar_dados_investimentos_csv()
)
def test_criar_investimentos_ddt_csv(
    base_url, auth_headers, asset, amount, price, days, planned, status_esperado
):
    """Executa multiplos cenarios de criacao de investimentos via CSV."""
    payload = {
        "asset_name": asset,
        "amount": amount,
        "purchase_price": price,
        "days_invested": days,
        "planned_days": planned,
    }

    response = requests.post(
        f"{base_url}/api/investments", json=payload, headers=auth_headers
    )

    assert response.status_code == status_esperado, response.text

    # Limpeza: remove o investimento criado para não acumular dados
    if response.status_code == 201:
        requests.delete(
            f"{base_url}/api/investments/{response.json()['id']}",
            headers=auth_headers,
        )
