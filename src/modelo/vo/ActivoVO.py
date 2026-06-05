class ActivoVO:
    def __init__(self, simbolo, nombre, precio, tipo):
        self.__simbolo = simbolo
        self.__nombre = nombre
        self.__precio = precio
        self.__tipo = tipo

    @property
    def simbolo(self): return self.__simbolo
    @property
    def nombre(self): return self.__nombre
    @property
    def precio(self): return self.__precio
    @property
    def tipo(self): return self.__tipo