class AvisoVO:
    def __init__(self, titulo, cuerpo):
        self.__titulo = titulo
        self.__cuerpo = cuerpo

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, v):
        self.__titulo = v

    @property
    def cuerpo(self):
        return self.__cuerpo

    @cuerpo.setter
    def cuerpo(self, v):
        self.__cuerpo = v

    def __repr__(self):
        return f"AvisoVO(titulo={self.__titulo})"