import pytest

from loja.produto import Calca, Camiseta, Produto


def test_camiseta_e_um_produto():
    assert isinstance(Camiseta("Camiseta básica", 39.90, "M", "curta"), Produto)


def test_camiseta_herda_a_validacao_do_produto():
    with pytest.raises(ValueError):
        Camiseta("Camiseta básica", -10, "M", "curta")


def test_manga_invalida():
    with pytest.raises(ValueError):
        Camiseta("Camiseta básica", 39.90, "M", "regata")


def test_descricao_sobrescrita_reaproveita_a_mae():
    calca = Calca("Calça jeans", 129.90, "G", "reta")
    assert calca.descricao() == "Calça jeans G: R$ 129.90 · reta"