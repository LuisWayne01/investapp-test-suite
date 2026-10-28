import requests

YIELD_MONTHLY_URL = "/api/simulate/yield-monthly"


# ===== Integrante 5: simulação de rendimento mensal =====
def test_yield_monthly_sucesso(base_url, auth_headers):
    """Simulação válida (12 meses) retorna 200 e corpo com resultado."""
    investimento = {
        "asset_name": "CDB",
        "amount": 1000.00,
        "purchase_price": 1.00,
        "days_invested": 30,
        "planned_days": 365,
    }
    cadastro = requests.post(
        f"{base_url}/api/investments",
        json=investimento,
        headers=auth_headers,
        timeout=30,
    )
    assert cadastro.status_code == 201, cadastro.text
    investment_id = cadastro.json()["id"]

    try:
        response = requests.post(
            f"{base_url}{YIELD_MONTHLY_URL}",
            json={"months": 12},
            headers=auth_headers,
            timeout=30,
        )
        assert response.status_code == 200, response.text
        data = response.json()
        print(data)
        assert isinstance(data, (dict, list))
        assert len(data) > 0, "A simulação retornou um corpo vazio."
    finally:
        requests.delete(
            f"{base_url}/api/investments/{investment_id}",
            headers=auth_headers,
            timeout=30,
        )


def test_yield_monthly_sem_autenticacao(base_url):
    """Sem token, a API deve recusar a requisição (401 ou 403)."""
    response = requests.post(
        f"{base_url}{YIELD_MONTHLY_URL}",
        json={},
        timeout=30,
    )
    assert response.status_code in (401, 403), response.text


# ===== Integrante 6: simulação de Resgate Otimizado Tributariamente =====
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
