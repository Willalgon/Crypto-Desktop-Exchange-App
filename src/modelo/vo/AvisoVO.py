class AvisoVO:
    def __init__(self, titulo, cuerpo):
        self.__titulo = titulo
        self.__cuerpo = cuerpo

    @property
    def titulo(self): return self.__titulo
    @property
    def cuerpo(self): return self.__cuerpo

    def __repr__(self):
        return f"AvisoVO(titulo={self.__titulo})"