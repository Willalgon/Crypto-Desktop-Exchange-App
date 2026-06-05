class OperacionVO:
    """
    Transporta los parámetros de una orden de compra o venta.

    Atributos
    ----------
    id_usuario  : int   — identificador del Trader que opera
    id_activo   : int   — identificador del activo a comprar/vender
    tipo        : str   — 'COMPRA' o 'VENTA'
    cantidad    : float — unidades del activo a operar
    """

    def __init__(self, id_usuario: int, id_activo: int, tipo: str, cantidad: float):
        self.id_usuario = id_usuario
        self.id_activo  = id_activo
        self.tipo       = tipo          # 'COMPRA' | 'VENTA'
        self.cantidad   = cantidad

    def __repr__(self):
        return (f"OperacionVO(id_usuario={self.id_usuario}, "
                f"id_activo={self.id_activo}, tipo={self.tipo}, "
                f"cantidad={self.cantidad})")



