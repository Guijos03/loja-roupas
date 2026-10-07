import pytest

from loja.carrinho import Carrinho
from loja.produto import Produto
from loja.promocao import Cupom, Percentual, SemPromocao


def carrinho_com(promocao):
    c = Carrinho(promocao)
    c.adicionar(Produto("Camiseta básica", 39.90, "M"), 3)
    c.adicionar(Produto("Calça jeans", 129.90, "G"))
    return c

@pytest.mark.parametrize("promocao, esperado", [
    (SemPromocao(), 249.60),
    (Percentual(10), 224.64), 
    (Cupom(100), 164.60), 
])
def test_total_com_cada_promocao(promocao, esperado):
    assert carrinho_com(promocao).total == pytest.approx(esperado)
