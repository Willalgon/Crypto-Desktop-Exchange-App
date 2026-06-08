class NoticiaVO:
    def __init__(self, titulo, cuerpo, es_aviso):
        self.__titulo = titulo
        self.__cuerpo = cuerpo
        self.__es_aviso = es_aviso

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

    @property
    def es_aviso(self):
        return self.__es_aviso

    @es_aviso.setter
    def es_aviso(self, v):
        self.__es_aviso = v