class ActivoVO:
    def __init__(self, id_activo=None, nombre=None, simbolo=None,
                 precio_actual=None, descripcion_especial=None, es_cripto=True):
        self.__id_activo = id_activo
        self.__nombre = nombre
        self.__simbolo = simbolo
        self.__precio_actual = float(precio_actual) if precio_actual is not None else None
        self.__descripcion_especial = descripcion_especial
        self.__es_cripto = bool(es_cripto) if es_cripto is not None else True
        self.__historial_precios = []

    @property
    def id_activo(self):
        return self.__id_activo

    @id_activo.setter
    def id_activo(self, s):
        self.__id_activo = s

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, v):
        self.__nombre = v

    @property
    def simbolo(self):
        return self.__simbolo

    @simbolo.setter
    def simbolo(self, v):
        self.__simbolo = v

    @property
    def precio_actual(self):
        return self.__precio_actual

    @precio_actual.setter
    def precio_actual(self, v):
        self.__precio_actual = float(v)

    @property
    def descripcion_especial(self):
        return self.__descripcion_especial

    @descripcion_especial.setter
    def descripcion_especial(self, v):
        self.__descripcion_especial = v

    @property
    def es_cripto(self):
        return self.__es_cripto

    @es_cripto.setter
    def es_cripto(self, v):
        self.__es_cripto = bool(v) if v is not None else True

    @property
    def historial_precios(self):
        return self.__historial_precios

    @historial_precios.setter
    def historial_precios(self, lista):
        self.__historial_precios = lista

    def __repr__(self):
        return f"ActivoVO(id={self.__id_activo}, simbolo={self.__simbolo}, precio={self.__precio_actual})"