class CarteraVO:
    def __init__(self, saldo_fiat, valor_activos, patrimonio_total):
        self.__saldo_fiat       = float(saldo_fiat)
        self.__valor_activos    = float(valor_activos)
        self.__patrimonio_total = float(patrimonio_total)

    @property
    def saldo_fiat(self):       return self.__saldo_fiat
    @property
    def valor_activos(self):    return self.__valor_activos
    @property
    def patrimonio_total(self): return self.__patrimonio_total

    def __repr__(self):
        return f"CarteraVO(fiat={self.__saldo_fiat}, patrimonio={self.__patrimonio_total})"