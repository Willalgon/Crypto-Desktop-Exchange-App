class PosicionVO:
    def __init__(self, simbolo, activo, cantidad, precio_medio_compra,
                 precio_actual, pnl, roi):
        self.__simbolo = simbolo
        self.__activo = activo
        self.__cantidad = float(cantidad)
        self.__precio_medio_compra = float(precio_medio_compra)
        self.__precio_actual = float(precio_actual)
        self.__pnl = float(pnl)
        self.__roi = float(roi)

    @property
    def simbolo(self):
        return self.__simbolo

    @simbolo.setter
    def simbolo(self, v):
        self.__simbolo = v

    @property
    def activo(self):
        return self.__activo

    @activo.setter
    def activo(self, v):
        self.__activo = v

    @property
    def cantidad(self):
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, v):
        self.__cantidad = float(v)

    @property
    def precio_medio_compra(self):
        return self.__precio_medio_compra

    @precio_medio_compra.setter
    def precio_medio_compra(self, v):
        self.__precio_medio_compra = float(v)

    @property
    def precio_actual(self):
        return self.__precio_actual

    @precio_actual.setter
    def precio_actual(self, v):
        self.__precio_actual = float(v)

    @property
    def pnl(self):
        return self.__pnl

    @pnl.setter
    def pnl(self, v):
        self.__pnl = float(v)

    @property
    def roi(self):
        return self.__roi

    @roi.setter
    def roi(self, v):
        self.__roi = float(v)

    def __repr__(self):
        return f"PosicionVO({self.__simbolo}, cant={self.__cantidad}, roi={self.__roi}%)"