class EventoMercadoVO:
    """Value Object para un evento de mercado lanzado por el admin."""

    EVENTOS_VALIDOS = [
        "Bull Market",
        "Bear Market",
        "Crisis Fiat",
        "Guerra Mundial",
        "Analista Aleatorio",
        "Inyección Liquidez",
        "Retirada Liquidez",
        "Halving Bitcoin",
        "Adopción Corporativa",
        "Adopción Países",
        "Crisis Bancaria",
        "Regulación China",
        "Hack Exchange",
        "Upgrade Ethereum",
        "Whale Dump",
        "Inflación Alta",
        "Fed Sube Tipos",
    ]

    def __init__(self, nombre_evento=None, descripcion=None, id_admin=None):
        self.__nombre_evento = nombre_evento
        self.__descripcion   = descripcion
        self.__id_admin      = id_admin

    @property
    def nombre_evento(self): return self.__nombre_evento
    @property
    def descripcion(self):   return self.__descripcion
    @property
    def id_admin(self):      return self.__id_admin

    def es_valido(self):
        return (
            self.__nombre_evento in self.EVENTOS_VALIDOS
            and bool(self.__descripcion and self.__descripcion.strip())
            and self.__id_admin is not None
        )

    def __repr__(self):
        return f"EventoMercadoVO(nombre={self.__nombre_evento}, admin={self.__id_admin})"