class CarteraVO:
    def __init__(self, saldo_fiat, valor_activos, patrimonio_total):
        self.__saldo_fiat = float(saldo_fiat)
        self.__valor_activos = float(valor_activos)
        self.__patrimonio_total = float(patrimonio_total)

    @property
    def saldo_fiat(self):
        return self.__saldo_fiat

    @saldo_fiat.setter
    def saldo_fiat(self, v):
        self.__saldo_fiat = float(v)

    @property
    def valor_activos(self):
        return self.__valor_activos

    @valor_activos.setter
    def valor_activos(self, v):
        self.__valor_activos = float(v)

    @property
    def patrimonio_total(self):
        return self.__patrimonio_total

    @patrimonio_total.setter
    def patrimonio_total(self, v):
        self.__patrimonio_total = float(v)

    def __repr__(self):
        return f"CarteraVO(fiat={self.__saldo_fiat}, patrimonio={self.__patrimonio_total})"