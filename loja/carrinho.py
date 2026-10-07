from loja.calculo import frete, total_carrinho
from loja.produto import Produto
from loja.promocao import SemPromocao


class Carrinho:
    def __init__(self, promocao=None):
        self._itens = []
        self._finalizado = False
        self._promocao = promocao if promocao is not None else SemPromocao()

    def adicionar(self, produto, quantidade=1):
        if self._finalizado:
            raise CarrinhoFinalizadoError("carrinho finalizado não recebe peças")
        if not isinstance(produto, Produto):
            raise TypeError("só é possível adicionar um Produto")
        if quantidade <= 0:
            raise ValueError("quantidade deve ser positiva")
        self._itens.append((produto, quantidade))

    @property
    def itens(self):
        return list(self._itens)

    @property
    def quantidade_de_pecas(self):
        return sum(quantidade for _, quantidade in self._itens)

    @property
    def subtotal(self):
        return total_carrinho([(p.preco, q) for p, q in self._itens])

    @property
    def total(self):
        valor = self._promocao.aplicar(self.subtotal)
        return valor + frete(valor)

    def finalizar(self):
        if not self._itens:
            raise ValueError("não é possível finalizar um carrinho vazio")
        self._finalizado = True