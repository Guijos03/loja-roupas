import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from api import app, obter_sessao, popular_se_vazio
from loja.banco import criar_tabelas, engine_em_memoria
from loja.repositorio import RepositorioProdutos
from loja.servico import ServicoCatalogo

cliente = TestClient(app)  


@pytest.fixture(autouse=True)
def banco_de_teste():
    """Cada teste ganha um banco novo, na memória, com os 3 produtos."""
    engine = engine_em_memoria()
    criar_tabelas(engine)
    with Session(engine) as sessao:
        popular_se_vazio(ServicoCatalogo(RepositorioProdutos(sessao)))

    def sessao_de_teste():
        with Session(engine) as sessao:
            yield sessao

    app.dependency_overrides[obter_sessao] = sessao_de_teste   # troca o banco
    cliente.delete("/carrinho")
    yield
    app.dependency_overrides.clear()


NOVO = {"tipo": "Produto", "nome": "Boné", "preco": 49.90, "tamanho": "M"}


def test_vitrine_tem_tres_produtos():
    resposta = cliente.get("/produtos")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 3


def test_produto_inexistente_da_404():
    assert cliente.get("/produtos/99").status_code == 404


def test_filtro_por_tamanho():
    nomes = [p["nome"] for p in cliente.get("/produtos", params={"tamanho": "M"}).json()]
    assert nomes == ["Camiseta básica"]


def test_cadastrar_da_201_e_aparece_na_lista():
    resposta = cliente.post("/produtos", json=NOVO)
    assert resposta.status_code == 201
    assert resposta.json()["id"] == 4
    assert len(cliente.get("/produtos").json()) == 4


def test_nome_repetido_da_409():
    cliente.post("/produtos", json=NOVO)
    assert cliente.post("/produtos", json=NOVO).status_code == 409


def test_regra_do_dominio_da_422():
    assert cliente.post("/produtos", json={**NOVO, "tamanho": "XL"}).status_code == 422


def test_atualizar_preco():
    resposta = cliente.put("/produtos/3", json={"tipo": "Produto", "nome": "Moletom",
                                                "preco": 139.90, "tamanho": "P"})
    assert resposta.status_code == 200
    assert cliente.get("/produtos/3").json()["preco"] == 139.90


def test_remover_da_204_e_depois_404():
    assert cliente.delete("/produtos/3").status_code == 204
    assert cliente.get("/produtos/3").status_code == 404


def test_quantidade_zero_da_422():
    resposta = cliente.post("/carrinho/itens", json={"produto_id": 1, "quantidade": 0})
    assert resposta.status_code == 422


def test_adicionar_item_da_201():
    resposta = cliente.post("/carrinho/itens", json={"produto_id": 1, "quantidade": 3})
    assert resposta.status_code == 201
    assert resposta.json()["pecas_no_carrinho"] == 3


def test_total_com_promocao_sem_frete():
    cliente.post("/carrinho/itens", json={"produto_id": 1, "quantidade": 3})
    cliente.post("/carrinho/itens", json={"produto_id": 2, "quantidade": 1})
    assert cliente.get("/carrinho/total").json() == {
        "pecas": 4, "subtotal": 249.6, "total": 224.64}


def test_total_abaixo_de_200_paga_frete():
    cliente.post("/carrinho/itens", json={"produto_id": 1, "quantidade": 1})
    assert cliente.get("/carrinho/total").json()["total"] == 50.91