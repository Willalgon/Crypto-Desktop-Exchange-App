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

    @property
    def nombre(self):
        return self.__nombre

    @property
    def simbolo(self):
        return self.__simbolo

    @property
    def precio_actual(self):
        return self.__precio_actual

    @property
    def descripcion_especial(self):
        return self.__descripcion_especial

    @property
    def es_cripto(self):
        return self.__es_cripto

    @property
    def historial_precios(self):
        return self.__historial_precios  # [(precio, fecha_hora), ...]

    @precio_actual.setter
    def precio_actual(self, v):
        self.__precio_actual = float(v)

    @historial_precios.setter
    def historial_precios(self, lista):
        self.__historial_precios = lista

    def __repr__(self):
        return f"ActivoVO(id={self.__id_activo}, simbolo={self.__simbolo}, precio={self.__precio_actual})"