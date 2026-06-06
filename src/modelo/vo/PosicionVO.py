class PosicionVO:
    def __init__(self, simbolo, activo, cantidad, precio_medio_compra,
                 precio_actual, pnl, roi):
        self.__simbolo              = simbolo
        self.__activo               = activo
        self.__cantidad             = float(cantidad)
        self.__precio_medio_compra  = float(precio_medio_compra)
        self.__precio_actual        = float(precio_actual)
        self.__pnl                  = float(pnl)
        self.__roi                  = float(roi)

    @property
    def simbolo(self):             return self.__simbolo
    @property
    def activo(self):              return self.__activo
    @property
    def cantidad(self):            return self.__cantidad
    @property
    def precio_medio_compra(self): return self.__precio_medio_compra
    @property
    def precio_actual(self):       return self.__precio_actual
    @property
    def pnl(self):                 return self.__pnl
    @property
    def roi(self):                 return self.__roi

    def __repr__(self):
        return f"PosicionVO({self.__simbolo}, cant={self.__cantidad}, roi={self.__roi}%)"