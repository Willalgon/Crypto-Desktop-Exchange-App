from abc import ABC, abstractmethod
from ConvertirBase import ConvertirBase

class Factura(ConvertirBase, ABC):
    contador = 0

    def __init__(self):
        super().__init__()
        Factura.contador += 1
        self.numero = Factura.contador
    def normalizar_importe(self, total: float, moneda: str = "USD"):
        if moneda == "USD":
            return self.euros_a_dolares(total)
        return round(total, 2)
    
    @abstractmethod
    def emitir(self, pedido):
        pass




class Pedido:
    contador = 0 

    def __init__(self, cliente: str, total: float):
        Pedido.contador += 1
        self.id = 1
        self.cliente = cliente
        self.total = total 
        self.item = []
        self.estado = "PENDIENTE"



    def añadirElemento(self, item):
        self.item.append(item)
    def modificarEstado(self, estado):
        self.estado = estado

    @property
    def total(self) -> float:
        return self._total
    @total.setter
    def total(self, value: float):
        if value < 0:
            raise ValueError("El total no puede ser negativo")
        self._total = value
# CryptoLearning app
## Login.py
1. Mostrar el login.ui
2. Llamar al controlador para autenticar
3. Redirigir a la ventana correcta según el rol.
