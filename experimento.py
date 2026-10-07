from loja.carrinho import Carrinho
from loja.produto import Produto
from loja.promocao import Promocao


class BlackFriday(Promocao):
    def aplicar_desconto(self, subtotal):  # nome errado de propósito
        return subtotal * 0.5


c = Carrinho(BlackFriday())  # aqui deve estourar o TypeError
c.adicionar(Produto("Moletom", 159.90, "P"))
print("carrinho montado")  # não deve aparecer
print(c.total)