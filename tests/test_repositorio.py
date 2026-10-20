import pytest
from sqlmodel import Session

from loja.banco import criar_engine, criar_tabelas, engine_em_memoria
from loja.produto import Calca, Camiseta, Produto
from loja.repositorio import RepositorioProdutos


@pytest.fixture
def repo():
    engine = engine_em_memoria()
    criar_tabelas(engine)
    with Session(engine) as sessao:
        yield RepositorioProdutos(sessao)


def test_adicionar_devolve_id(repo):
    assert repo.adicionar(Produto("Moletom", 159.90, "P")) == 1


def test_buscar_devolve_objeto_do_dominio(repo):
    produto_id = repo.adicionar(Camiseta("Camiseta básica", 39.90, "M", "curta"))
    camiseta = repo.buscar(produto_id)
    assert isinstance(camiseta, Camiseta)
    assert camiseta.manga == "curta"


def test_buscar_inexistente_devolve_none(repo):
    assert repo.buscar(99) is None


def test_listar_com_filtro(repo):
    repo.adicionar(Camiseta("Camiseta básica", 39.90, "M", "curta"))
    repo.adicionar(Calca("Calça jeans", 129.90, "G", "reta"))
    nomes = [p.nome for _, p in repo.listar(preco_max=100)]
    assert nomes == ["Camiseta básica"]


def test_atualizar_e_remover(repo):
    produto_id = repo.adicionar(Produto("Moletom", 159.90, "P"))
    assert repo.atualizar(produto_id, Produto("Moletom", 139.90, "P"))
    assert repo.buscar(produto_id).preco == 139.90
    assert repo.remover(produto_id)
    assert repo.buscar(produto_id) is None


def test_dados_sobrevivem_ao_reinicio(tmp_path):
    url = f"sqlite:///{tmp_path / 'loja.db'}"
    engine = criar_engine(url)
    criar_tabelas(engine)
    with Session(engine) as sessao:
        RepositorioProdutos(sessao).adicionar(Produto("Moletom", 159.90, "P"))
    engine.dispose()                      # "desliga o servidor"

    outro = criar_engine(url)             # "liga de novo"
    with Session(outro) as sessao:
        assert RepositorioProdutos(sessao).buscar(1).nome == "Moletom"