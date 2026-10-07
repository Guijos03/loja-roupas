from abc import ABC, abstractmethod

class Promocao(ABC):

    @abstractmethod
    def aplicar(self, subtotal):
        pass



class SemPromocao(Promocao):
    def aplicar(self, subtotal):
        return subtotal


class Percentual(Promocao):
    def __init__(self, percentual):
        if not 0 <= percentual <= 100:
            raise ValueError("percentual deve estar entre 0 e 100")
        self.percentual = percentual

    def aplicar(self, subtotal):
        return subtotal * (1 - self.percentual / 100)


class Cupom(Promocao):
    def __init__(self, valor):
        if valor <= 0:
            raise ValueError("valor do cupom deve ser positivo")
        self.valor = valor

    def aplicar(self, subtotal):
        return max(0.0, subtotal - self.valor)