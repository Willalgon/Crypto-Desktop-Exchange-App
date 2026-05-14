class NoticiaVO:
    def __init__(self, titulo, cuerpo, es_aviso):
        self.__titulo = titulo
        self.__cuerpo = cuerpo
        self.__es_aviso = es_aviso

    @property
    def titulo(self):
        return self.__titulo

    @property
    def cuerpo(self):
        return self.__cuerpo

    @property
    def es_aviso(self):
        return self.__es_aviso