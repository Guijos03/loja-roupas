import pytest

from loja.carrinho import Carrinho, CarrinhoFinalizadoError
from loja.produto import Produto


def carrinho_exemplo():
    c = Carrinho()
    c.adicionar(Produto("Camiseta básica", 39.90, "M"), 3)
    c.adicionar(Produto("Calça jeans", 129.90, "G"))
    return c


def test_subtotal_e_quantidade():
    c = carrinho_exemplo()
    assert c.quantidade_de_pecas == 4
    assert c.subtotal == pytest.approx(249.60)


def test_acima_de_200_frete_gratis():
    assert carrinho_exemplo().total == pytest.approx(249.60)


def test_abaixo_de_200_paga_frete():
    c = Carrinho()
    c.adicionar(Produto("Camiseta básica", 39.90, "M"))
    assert c.total == pytest.approx(54.90)


def test_quantidade_zero_nao_entra():
    with pytest.raises(ValueError):
        Carrinho().adicionar(Produto("Moletom", 159.90, "P"), 0)


def test_so_aceita_produto():
    with pytest.raises(TypeError):
        Carrinho().adicionar(("Moletom", 159.90))


def test_finalizado_nao_recebe_pecas():
    c = carrinho_exemplo()
    c.finalizar()
    with pytest.raises(CarrinhoFinalizadoError):
        c.adicionar(Produto("Moletom", 159.90, "P"))


def test_itens_devolve_copia():
    c = carrinho_exemplo()
    c.itens.append("intruso")
    assert len(c.itens) == 2