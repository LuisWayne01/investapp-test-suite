
import requests


def test_simulacao_resgate_otimizado_tributariamente(base_url, auth_headers):
    """Testa a simulação de resgate com otimização tributária."""

    investimento = {
        "asset_name": "CDB",
        "amount": 1000,
        "purchase_price": 1000,
        "days_invested": 30,
        "planned_days": 365,
    }

    cadastro = requests.post(
        f"{base_url}/api/investments",
        json=investimento,
        headers=auth_headers,
        timeout=30,
    )

    assert cadastro.status_code == 201, (
        f"Falha ao cadastrar investimento: "
        f"HTTP {cadastro.status_code} - {cadastro.text}"
    )

    investment_id = cadastro.json()["id"]

    try:
        response = requests.post(
            f"{base_url}/api/simulate/tax-withdrawal",
            json={"target_amount": 1000},
            headers=auth_headers,
            timeout=30,
        )

        assert response.status_code == 200, (
            f"Esperado HTTP 200, recebido {response.status_code}. "
            f"Resposta da API: {response.text}"
        )

    finally:
        exclusao = requests.delete(
            f"{base_url}/api/investments/{investment_id}",
            headers=auth_headers,
            timeout=30,
        )

        assert exclusao.status_code == 200, (
            f"Falha ao excluir investimento temporário: "
            f"HTTP {exclusao.status_code} - {exclusao.text}"
        )
