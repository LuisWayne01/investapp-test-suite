import requests


def test_openapi_swagger_contract(base_url):
    """[Aluno 9] Valida se a documentação Swagger/OpenAPI da API está online."""
    response = requests.get(f"{base_url}/docs")
    assert response.status_code == 200, (
        f"Documentação Swagger indisponível: HTTP {response.status_code}"
    )


def test_fluxo_completo_ciclo_de_vida_investimento(base_url, auth_headers):
    """[Aluno 9] Teste E2E: Executa a jornada completa de um investimento."""
    # 1. Criar novo investimento com ativo válido ("CDB")
    payload_criar = {
        "asset_name": "CDB",
        "amount": 2500.00,
        "purchase_price": 1.00,
        "days_invested": 90,
        "planned_days": 365,
    }
    res_criar = requests.post(
        f"{base_url}/api/investments", json=payload_criar, headers=auth_headers
    )
    assert res_criar.status_code in [
        200,
        201,
    ], f"Erro ao criar investimento: {res_criar.text}"

    dados_criados = res_criar.json()
    investment_id = dados_criados.get("id") or dados_criados.get(
        "investment_id"
    )
    assert (
        investment_id is not None
    ), "A resposta não retornou o ID do investimento."

    try:
        # 2. Listar investimentos e confirmar a presença do item criado
        res_listar = requests.get(
            f"{base_url}/api/investments", headers=auth_headers
        )
        assert res_listar.status_code == 200
        lista_investimentos = res_listar.json()

        ids_na_lista = [
            item.get("id") or item.get("investment_id")
            for item in lista_investimentos
        ]
        assert (
            investment_id in ids_na_lista
        ), f"O investimento ID {investment_id} não foi encontrado na listagem."

        # 3. Executar chamada no módulo de simulação
        payload_simular = {"months": 12}
        res_simular = requests.post(
            f"{base_url}/api/simulate/yield-monthly",
            json=payload_simular,
            headers=auth_headers,
        )
        assert res_simular.status_code == 200, (
            f"Falha na simulação: HTTP {res_simular.status_code} - "
            f"{res_simular.text}"
        )

    finally:
        # 4. Limpeza (Teardown) - Excluir o investimento criado
        if investment_id:
            res_deletar = requests.delete(
                f"{base_url}/api/investments/{investment_id}",
                headers=auth_headers,
            )
            assert res_deletar.status_code in [
                200,
                204,
            ], f"Falha ao excluir investimento ID {investment_id}: {res_deletar.text}"
