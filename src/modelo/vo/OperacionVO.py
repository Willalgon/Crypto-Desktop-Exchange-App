class OperacionVO:
    def __init__(self, id_usuario: int, id_activo: int, tipo: str, cantidad: float):
        self.__id_usuario = id_usuario
        self.__id_activo = id_activo
        self.__tipo = tipo
        self.__cantidad = cantidad

    @property
    def id_usuario(self):
        return self.__id_usuario

    @id_usuario.setter
    def id_usuario(self, v):
        self.__id_usuario = v

    @property
    def id_activo(self):
        return self.__id_activo

    @id_activo.setter
    def id_activo(self, v):
        self.__id_activo = v

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, v):
        self.__tipo = v

    @property
    def cantidad(self):
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, v):
        self.__cantidad = v

    def __repr__(self):
        return (f"OperacionVO(id_usuario={self.__id_usuario}, "
                f"id_activo={self.__id_activo}, tipo={self.__tipo}, "
                f"cantidad={self.__cantidad})")