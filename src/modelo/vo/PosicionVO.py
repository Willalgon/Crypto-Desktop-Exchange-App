class PosicionVO:
    def __init__(self, simbolo, cantidad, precio_medio_compra, pnl, roi):
        self.__simbolo = simbolo
        self.__cantidad = cantidad
        self.__precio_medio_compra = precio_medio_compra
        self.__pnl = pnl
        self.__roi = roi

    @property
    def simbolo(self): return self.__simbolo
    
    @property
    def cantidad(self): return self.__cantidad
    
    @property
    def precio_medio_compra(self): return self.__precio_medio_compra
    
    @property
    def pnl(self): return self.__pnl
    
    @property
    def roi(self): return self.__roi